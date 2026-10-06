# storyboard-ledger

Dedicated tooling repo: Markdown storyboard shot-list → image-generation prompt pipeline.

**Engine status:** `storyboard_to_prompts.py` v1.3 — **LOCKED** per GFED ruling 2026-10-06
(v1.3 bug-fix cycle: see `docs/pipeline-verification-signoff.md`).
Scope: core parsing logic, 9:16 default aspect ratio, orthogonal camera/speed tag expansion,
fallback token preservation, segment-based Markdown table normalization.
Invariant: any future modification to base token mappings or row-ingestion behavior
requires an explicit version bump and sign-off cycle.

## Contents

| Path | What it is |
|---|---|
| `storyboard_to_prompts.py` | The locked parser. Markdown storyboard tables → positive/negative prompts + JSON/CSV/TXT manifests. |
| `automation/watch_storyboards.py` | Local watcher (zero dependencies, mtime polling). Auto-generates manifests on `.md` change; fail-closed error logs never overwrite existing manifests. |
| `.github/workflows/storyboard_manifest.yml` | CI: validates every scene file with `--strict` on push/PR; fails the build on malformed tables; commits manifests back. |
| `tests/` | Parser regression tests: `python3 -m unittest discover -s tests` (run in CI by `parser_tests.yml`). |
| `docs/` | Reference: ledger definition, script-to-storyboard decomposition, shot-list template, verification sign-off. |

## Quick start

```bash
# Single file
python3 storyboard_to_prompts.py scenes/scene_04.md -c "Grim sci-fi interior, amber and teal backlight"

# Strict validation (watcher / CI mode — exits non-zero on malformed tables, writes nothing)
python3 storyboard_to_prompts.py scenes/scene_04.md --strict

# Watch a directory
python3 automation/watch_storyboards.py scenes/

# Override aspect ratio (default 9:16)
python3 storyboard_to_prompts.py scenes/scene_04.md --ar 4:5
```

## Pipeline

Shot-list template → `storyboard_to_prompts.py` → `.json` / `.csv` / `.txt` manifests → downstream generation nodes.

Panel IDs (e.g. `SC04-P01`) are the primary key shared with the Master Storyboard Ledger:
one template row → one ledger row, carrying status (DRAFT / STAGED / LOCKED / SUPERSEDED),
version, and ruling authority.
