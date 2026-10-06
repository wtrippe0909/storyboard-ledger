#!/usr/bin/env python3
"""
Storyboard watcher — Option 1 local automation (GFED authorized 2026-10-06).

Monitors a directory for .md storyboard files. On modification, runs
storyboard_to_prompts.py in --strict mode:
  - success -> writes .json / .csv / .txt manifests next to the source file
  - failure -> writes a .storyboard-errors.log, leaves existing manifests untouched

Zero external dependencies: lightweight mtime polling loop (no watchdog).

Usage:
  python3 watch_storyboards.py scenes/                  # watch forever, 2s poll
  python3 watch_storyboards.py scenes/ --interval 5
  python3 watch_storyboards.py scenes/ --once            # single scan pass (cron/CI)
  python3 watch_storyboards.py scenes/ --ar 4:5 -c "context prompt"
"""

import argparse
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path


def find_parser() -> Path:
    """Locate storyboard_to_prompts.py next to this watcher or in its parent dir."""
    here = Path(__file__).resolve().parent
    for candidate in (here / "storyboard_to_prompts.py",
                      here.parent / "storyboard_to_prompts.py"):
        if candidate.exists():
            return candidate
    raise FileNotFoundError(
        "storyboard_to_prompts.py not found next to watch_storyboards.py "
        "or in its parent directory"
    )


def error_log_path(md_file: Path) -> Path:
    return md_file.with_suffix(".storyboard-errors.log")


def clear_error_log(md_file: Path) -> None:
    log = error_log_path(md_file)
    if log.exists():
        log.unlink()


def write_error_log(md_file: Path, errors: list[str]) -> None:
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    log = error_log_path(md_file)
    with open(log, "w", encoding="utf-8") as f:
        f.write(f"Storyboard validation FAILED: {md_file.name}\n")
        f.write(f"Time: {ts}\n")
        f.write("Existing manifests were NOT overwritten.\n\n")
        for err in errors:
            f.write(f"- {err}\n")


def process_file(md_file: Path, parser: Path, aspect_ratio: str, context: str) -> bool:
    """
    Run the parser in --strict mode on one file.
    Returns True on success (manifests written), False on validation failure
    (error log written, existing manifests untouched).
    """
    cmd = [
        sys.executable, str(parser), str(md_file),
        "--strict", "--ar", aspect_ratio,
    ]
    if context:
        cmd += ["-c", context]

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0:
        clear_error_log(md_file)
        print(f"[OK] {md_file.name}: manifests written.")
        return True

    # Fail closed: parse stderr/stdout for the error lines, log them.
    output = (result.stdout + "\n" + result.stderr).strip()
    errors = [
        line[4:].strip() if line.strip().startswith("- ") else line.strip()
        for line in output.splitlines()
        if line.strip() and not line.strip().startswith("STRICT VALIDATION FAILED")
    ] or ["Unknown parser failure (no error details captured)."]
    write_error_log(md_file, errors)
    print(f"[FAIL] {md_file.name}: validation failed -> {error_log_path(md_file).name}")
    return False


def scan_once(watch_dir: Path, parser: Path, aspect_ratio: str, context: str,
              state: dict) -> None:
    """Process any .md files whose mtime changed since the last scan."""
    for md_file in sorted(watch_dir.rglob("*.md")):
        if md_file.name.endswith(".storyboard-errors.log"):
            continue
        try:
            mtime = md_file.stat().st_mtime
        except OSError:
            continue
        if state.get(str(md_file)) != mtime:
            state[str(md_file)] = mtime
            process_file(md_file, parser, aspect_ratio, context)


def main() -> None:
    ap = argparse.ArgumentParser(description="Watch a directory and auto-generate storyboard manifests.")
    ap.add_argument("watch_dir", type=Path, help="Directory to monitor for .md storyboard files.")
    ap.add_argument("--interval", type=float, default=2.0, help="Poll interval in seconds (default: 2).")
    ap.add_argument("--once", action="store_true", help="Run a single scan pass and exit.")
    ap.add_argument("--ar", type=str, default="9:16", help="Aspect ratio passed to the parser.")
    ap.add_argument("-c", "--context", type=str, default="", help="Global scene context prompt.")
    args = ap.parse_args()

    if not args.watch_dir.is_dir():
        raise NotADirectoryError(f"Watch directory not found: {args.watch_dir}")

    parser = find_parser()
    state: dict = {}

    if args.once:
        scan_once(args.watch_dir, parser, args.ar, args.context, state)
        return

    print(f"Watching {args.watch_dir} every {args.interval}s (Ctrl+C to stop)...")
    try:
        while True:
            scan_once(args.watch_dir, parser, args.ar, args.context, state)
            time.sleep(args.interval)
    except KeyboardInterrupt:
        print("\nWatcher stopped.")


if __name__ == "__main__":
    main()
