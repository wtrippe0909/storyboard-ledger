#!/usr/bin/env python3
"""
Storyboard Markdown Table to Image Generation Prompt Parser (v1.2)
- Default aspect ratio: 9:16 (overridable via --ar)
- Comprehensive camera movement & speed expansion (PAN, TILT, ZOOM, WHIP, CRANE, BOOM, PUSH/PULL)
- Robust parser supporting both single-line <br> and multi-line markdown table rows
- v1.2 (2026-10-06, under GFED LOCKED ruling 2026-10-06 authorizing Option 1 automation):
  additive only — source line tracking per panel, header/column validation,
  --strict fail-closed mode. Token mappings and row-ingestion behavior unchanged.
Source: collaborator (Meta AI) patch, relayed via GFED, 2026-10-06.
Muse verification note (2026-10-06): normalize_markdown_table v1.1 failed on the
relayed multi-line format (row-start detection required >=5 pipes; relayed rows
start with 2). Replaced with segment-based normalization — see function docstring.
"""

import re
import csv
import json
import argparse
from pathlib import Path
from typing import List, Dict, Any, Optional, NamedTuple


class TableRow(NamedTuple):
    """A normalized table row: segment text plus 1-based source line range."""
    text: str
    start_line: int
    end_line: int


CAMERA_EXPANSIONS = {
    # Framing / Shot Size
    "ELS": "extreme wide shot, panoramic establishing view",
    "VWS": "very wide shot, vast perspective",
    "WS": "wide establishing shot, full environment visible",
    "FS": "full body shot, character head to toe in frame",
    "MS": "medium waist-up shot",
    "MCU": "medium close-up, chest and head view",
    "CU": "close-up portrait shot, detailed expression",
    "ECU": "extreme close-up macro shot, hyper-focused fine detail",
    "OTS": "over-the-shoulder perspective shot",
    "POV": "first-person point-of-view perspective",
    # Angles & Heights
    "EYE": "eye-level straight angle framing",
    "LOW": "dramatic low-angle perspective looking upward",
    "HIGH": "high-angle perspective looking downward",
    "DUTCH": "canted horizon, tilted Dutch angle composition",
    "CANTED": "tilted Dutch angle framing",
    "BIRD": "top-down overhead bird's eye view",
    "WORM": "ground-level worm's eye perspective",
    # Movements & Dynamics
    "STATIC": "stable composed camera framing",
    "DOLLY IN": "dolly push-in perspective creating visual depth",
    "DOLLY OUT": "dolly pull-out perspective revealing surroundings",
    "DOLLY": "dynamic directional camera push depth",
    "PUSH IN": "forward camera push-in focal zoom",
    "PULL OUT": "camera pulling back to reveal scene depth",
    "TRACK": "lateral tracking camera perspective",
    "TRUCK": "lateral tracking camera perspective",
    "PAN": "horizontal panning camera sweep",
    "TILT": "vertical tilting camera angle transition",
    "ZOOM IN": "optical zoom-in framing focus",
    "ZOOM OUT": "optical zoom-out expanding frame",
    "ZOOM": "optical focal zoom dynamic",
    "WHIP": "high-speed whip pan motion blur transition",
    "BOOM": "vertical boom jib crane elevation",
    "CRANE": "high sweeping crane camera movement",
    "HANDHELD": "gritty documentary handheld camera framing, subtle kinetic motion",
    "JITTER": "camera jitter, micro-shake tension"
}

BASE_STYLE_MODIFIERS = (
    "cinematic lighting, 35mm film grain, anamorphic lens flare, "
    "depth of field, atmospheric, hyper-detailed, photorealistic, 8k resolution"
)

DEFAULT_NEGATIVE_PROMPT = (
    "text, watermark, logo, typography, out of frame, deformed hands, "
    "distorted anatomy, low resolution, blurry, oversaturated, illustration artifacts"
)


def clean_markdown_cell(text: str) -> str:
    """Strip Markdown backticks, HTML tags, and redundant whitespace."""
    if not text:
        return ""
    text = re.sub(r"<br\s*/?>", " ", text)
    text = re.sub(r"[`*]", "", text)
    return " ".join(text.split()).strip()


def expand_camera_tags(framing_raw: str, movement_raw: str) -> str:
    """Map shorthand codes and movement descriptions to descriptive generative tokens."""
    expanded_tokens = []
    combined_raw = f"{framing_raw} {movement_raw}".upper()
    matched_keys = set()

    # Prioritize multi-word phrases first (e.g., 'PUSH IN' before 'IN', 'DOLLY IN' before 'DOLLY')
    sorted_keys = sorted(CAMERA_EXPANSIONS.keys(), key=lambda k: len(k.split()), reverse=True)

    for tag in sorted_keys:
        pattern = rf"\b{re.escape(tag)}\b"
        if re.search(pattern, combined_raw):
            if not any(tag in m for m in matched_keys):
                expanded_tokens.append(CAMERA_EXPANSIONS[tag])
                matched_keys.add(tag)

    # Capture modifiers like FAST, SLOW, RAPID
    if re.search(r"\bFAST\b|\bRAPID\b", combined_raw):
        expanded_tokens.append("high velocity motion")
    elif re.search(r"\bSLOW\b", combined_raw):
        expanded_tokens.append("slow deliberate movement")

    # If nothing matched, retain cleaned raw text so movement instructions are never lost
    if not expanded_tokens:
        clean_raw = f"{clean_markdown_cell(framing_raw)}, {clean_markdown_cell(movement_raw)}"
        return clean_raw.strip(", ")

    return ", ".join(expanded_tokens)


def parse_action_cell(action_cell_raw: str) -> Dict[str, str]:
    """Parse Subject, Action, and Focal Point labels from the action cell."""
    text = re.sub(r"<br\s*/?>", "\n", action_cell_raw)

    subject_match = re.search(r"Subject:\s*([^\n]+)", text, re.IGNORECASE)
    action_match = re.search(r"Action:\s*([^\n]+)", text, re.IGNORECASE)
    focal_match = re.search(r"Focal Point:\s*([^\n]+)", text, re.IGNORECASE)

    subject = clean_markdown_cell(subject_match.group(1)) if subject_match else ""
    action = clean_markdown_cell(action_match.group(1)) if action_match else ""
    focal = clean_markdown_cell(focal_match.group(1)) if focal_match else ""

    if not (subject or action or focal):
        action = clean_markdown_cell(action_cell_raw)

    return {"subject": subject, "action": action, "focal_point": focal}


def normalize_markdown_table(md_content: str) -> List["TableRow"]:
    """
    Normalize table rows into atomic single-line rows with <br> separators.

    Handles both single-line <br> tables and multi-line tables where cell
    content wraps onto physical lines that do not start with a pipe.

    Strategy: a new row begins at every physical line starting with '|'.
    Any non-pipe line that follows is a wrapped cell continuation and is
    appended to the current row. The relayed v1.1 implementation required
    >=5 pipes to detect a row start, which failed on the relayed format
    itself (rows like '| SC04-P01 | WS' carry only 2 pipes on the first
    physical line), silently dropping every row.

    Returns a list of TableRow(segment_text, start_line_1based, end_line_1based)
    so panels can carry source line numbers for fail-closed error reporting.
    """
    segments: List[TableRow] = []
    current: Optional[str] = None
    current_start: int = 0

    for lineno, raw in enumerate(md_content.splitlines(), start=1):
        line = raw.strip()
        if not line:
            continue
        if line.startswith("|"):
            if current is not None:
                segments.append(TableRow(current, current_start, lineno - 1))
            current = line
            current_start = lineno
        elif current is not None:
            # Wrapped cell continuation: fold into the current row.
            current += " <br> " + line

    if current is not None:
        # end line = last non-empty line number
        last = sum(1 for _ in md_content.splitlines())
        segments.append(TableRow(current, current_start, last))

    return segments


def parse_storyboard_markdown(
    md_content: str, global_context: str = "", aspect_ratio: str = "9:16"
) -> List[Dict[str, Any]]:
    """Parse table rows into prompt objects applying the configured aspect ratio."""
    panels = []
    rows = normalize_markdown_table(md_content)

    if len(rows) < 3:
        return panels

    for row in rows[2:]:
        cells = [c.strip() for c in row.text.split("|")[1:-1]]
        if len(cells) < 4:
            continue

        panel_id = clean_markdown_cell(cells[0])
        if not panel_id or panel_id.startswith("---"):
            continue

        framing_raw = cells[1] if len(cells) > 1 else ""
        movement_raw = cells[2] if len(cells) > 2 else ""
        action_raw = cells[3] if len(cells) > 3 else ""
        audio_raw = cells[4] if len(cells) > 4 else ""
        duration_raw = cells[5] if len(cells) > 5 else ""

        parsed_action = parse_action_cell(action_raw)
        camera_terms = expand_camera_tags(framing_raw, movement_raw)

        core_elements = []
        if parsed_action["subject"]:
            core_elements.append(parsed_action["subject"])
        if parsed_action["action"]:
            core_elements.append(parsed_action["action"])
        if parsed_action["focal_point"]:
            core_elements.append(f"focused on {parsed_action['focal_point']}")

        scene_description = ", ".join(core_elements)

        prompt_parts = []
        if global_context:
            prompt_parts.append(global_context)
        if camera_terms:
            prompt_parts.append(camera_terms)
        if scene_description:
            prompt_parts.append(scene_description)
        prompt_parts.append(BASE_STYLE_MODIFIERS)

        positive_prompt = ", ".join([p for p in prompt_parts if p])
        midjourney_prompt = f"/imagine prompt: {positive_prompt} --ar {aspect_ratio} --v 6.1"

        panels.append({
            "panel_id": panel_id,
            "source_lines": (
                f"{row.start_line}-{row.end_line}"
                if row.end_line != row.start_line
                else f"{row.start_line}"
            ),
            "duration": clean_markdown_cell(duration_raw),
            "camera_raw": f"{clean_markdown_cell(framing_raw)} | {clean_markdown_cell(movement_raw)}",
            "camera_expanded": camera_terms,
            "subject": parsed_action["subject"],
            "action": parsed_action["action"],
            "focal_point": parsed_action["focal_point"],
            "audio_cues": clean_markdown_cell(audio_raw),
            "positive_prompt": positive_prompt,
            "negative_prompt": DEFAULT_NEGATIVE_PROMPT,
            "midjourney_command": midjourney_prompt
        })

    return panels


REQUIRED_COLUMNS = [
    "panel",      # Panel ID
    "framing",    # Framing & Angle
    "movement",   # Movement
    "visual",     # Visual Action & Blocking
    "audio",      # Audio (Dialogue, VO, SFX, Score)
    "duration",   # Duration
    "transition", # Transition
]


def validate_markdown(md_content: str) -> List[str]:
    """
    Fail-closed validation for storyboard markdown.
    Returns a list of human-readable error strings (empty = valid).
    v1.2 addition under the Option 1 automation authorization.
    """
    errors: List[str] = []
    rows = normalize_markdown_table(md_content)

    if len(rows) < 3:
        errors.append("No parseable storyboard table found (need header + divider + at least one data row).")
        return errors

    header_cells = [clean_markdown_cell(h).lower() for h in rows[0].text.split("|")[1:-1]]
    header_joined = " | ".join(header_cells)
    for required in REQUIRED_COLUMNS:
        if not any(required in cell for cell in header_cells):
            errors.append(
                f"Header row (line {rows[0].start_line}) is missing a required column "
                f"matching '{required}'. Found columns: {header_joined or '(none)'}"
            )

    data_rows = rows[2:]
    parseable = 0
    for row in data_rows:
        cells = [c.strip() for c in row.text.split("|")[1:-1]]
        panel_id = clean_markdown_cell(cells[0]) if cells else ""
        if not panel_id or panel_id.startswith("---"):
            continue
        parseable += 1
        if len(cells) < 7:
            errors.append(
                f"Row '{panel_id}' (lines {row.start_line}-{row.end_line}) has "
                f"{len(cells)} cells; expected 7 (Panel ID, Framing & Angle, Movement, "
                f"Visual Action & Blocking, Audio, Duration, Transition)."
            )

    if parseable == 0:
        errors.append("Zero data rows parsed — check that table rows use '|' delimiters and Panel IDs are present.")

    return errors


def export_prompts(panels: List[Dict[str, Any]], output_base: Path):
    """Export parsed prompt payloads to JSON, CSV, and plain TXT."""
    json_path = output_base.with_suffix(".json")
    csv_path = output_base.with_suffix(".csv")
    txt_path = output_base.with_suffix(".txt")

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(panels, f, indent=2, ensure_ascii=False)

    fieldnames = [
        "panel_id", "source_lines", "duration", "camera_raw", "subject",
        "action", "focal_point", "positive_prompt",
        "negative_prompt", "midjourney_command"
    ]
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(panels)

    with open(txt_path, "w", encoding="utf-8") as f:
        for p in panels:
            f.write(f"// {p['panel_id']} ({p['duration']})\n")
            f.write(f"{p['midjourney_command']}\n\n")

    print(f"Exported {len(panels)} panels to:")
    print(f" - JSON: {json_path}")
    print(f" - CSV:  {csv_path}")
    print(f" - TXT:  {txt_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Convert Markdown storyboard tables into image generation prompts."
    )
    parser.add_argument("input_file", type=Path, help="Path to Markdown storyboard file.")
    parser.add_argument(
        "-o", "--output", type=Path, default=None,
        help="Base path for output files (default: same stem as input)"
    )
    parser.add_argument(
        "-c", "--context", type=str, default="",
        help="Global scene context or lighting prompt"
    )
    parser.add_argument(
        "--ar", type=str, default="9:16",
        help="Target aspect ratio for Midjourney flag (default: 9:16)"
    )
    parser.add_argument(
        "--strict", action="store_true",
        help="Fail-closed validation: exit non-zero and write nothing if the "
             "table fails validation or yields zero panels (for watchers/CI)."
    )

    args = parser.parse_args()

    if not args.input_file.exists():
        raise FileNotFoundError(f"Input file not found: {args.input_file}")

    content = args.input_file.read_text(encoding="utf-8")

    if args.strict:
        validation_errors = validate_markdown(content)
        if validation_errors:
            print(f"STRICT VALIDATION FAILED for {args.input_file}:")
            for err in validation_errors:
                print(f"  - {err}")
            raise SystemExit(2)

    context = args.context
    if not context:
        obj_match = re.search(r"\*\*Scene Objective:\*\*\s*([^\n]+)", content)
        if obj_match:
            context = obj_match.group(1).strip()

    panels = parse_storyboard_markdown(content, global_context=context, aspect_ratio=args.ar)

    if not panels:
        print("Warning: No storyboard table rows parsed. Verify table markdown syntax.")
        return

    out_base = args.output if args.output else args.input_file.with_suffix("")
    export_prompts(panels, out_base)


if __name__ == "__main__":
    main()
