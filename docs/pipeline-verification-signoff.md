# Storyboard Pipeline — Verification Sign-Off

**Script:** `storyboard_to_prompts.py` v1.2 (v1.1 + Muse normalizer fix + Option 1 additive changes)
**Filed:** 2026-10-06
**Source lineage:** Meta AI v1.0 → Muse test findings → Meta AI v1.1 patch → Muse bug fix + independent verification

## Verified checkpoints (all confirmed by Muse test runs 2026-10-06)

| Component | Status | Guarantee |
|---|---|---|
| Default Aspect Ratio | VERIFIED | Defaults to 9:16; `--ar` override works (tested 4:5) |
| Camera Movement Coverage | VERIFIED | PAN, TILT, ZOOM, WHIP, BOOM, CRANE, PUSH IN, PULL OUT all expand |
| Speed Modifiers | VERIFIED | FAST/SLOW/RAPID append orthogonal velocity descriptors; no token duplication ("fast" pruned from PUSH IN base) |
| Fallback Retention | VERIFIED | Unmapped camera/movement strings are sanitized and preserved, never silently dropped |
| Multi-Format Ingestion | VERIFIED | 5/5 single-line `<br>` rows; 3/3 multi-line relayed-format rows |

## Known deviation from the relayed patch

The relayed v1.1 `normalize_markdown_table` (pipe-count ≥ 5 row detection) silently parsed **zero panels** on the relayed multi-line format. Replaced with segment-based normalization (new row at every `|`-starting line; non-pipe lines folded as continuations). Fix documented in the script docstring.

## Governance note

**LOCKED per GFED ruling 2026-10-06** (relayed 16:54 EDT). Scope: core parsing logic, aspect-ratio handling (9:16 default), orthogonal camera/speed tag expansion, fallback token preservation, segment-based normalization. Invariant: any future modification to base token mappings or row-ingestion behavior requires an explicit version bump and sign-off cycle.

v1.2 (2026-10-06) was cut under the same ruling's Option 1 authorization: additive only — per-panel `source_lines`, header/column validation, `--strict` fail-closed mode. Token mappings and ingestion behavior unchanged.

## Option 1 build record (authorized 2026-10-06, built and verified same day)

- `automation/watch_storyboards.py` — local watcher, zero dependencies (mtime polling). `--once` for single-pass/CI use. Fail-closed: validation failure writes `.storyboard-errors.log`, leaves existing manifests untouched; fixing the file and re-running clears the log and writes manifests.
- `.github/workflows/storyboard_manifest.yml` — GitHub Action (env-configurable script path and scene glob). Validates with `--strict` on push/PR touching `**/*.md`; fails the build on malformed tables; commits manifests back on push, uploads as artifact on PRs.
- Target repo for the workflow file: `wtrippe0909/storyboard-ledger` (installed via handoff HA-20261006-SL-001).

## Proposed next steps

1. ~~**Automation / orchestration**~~ — BUILT (Option 1). Installed in `wtrippe0909/storyboard-ledger`.
2. **API integration** — PARKED until ComfyUI model architecture and node layout are defined (per GFED ruling 2026-10-06).
