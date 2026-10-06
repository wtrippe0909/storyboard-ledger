# Master Storyboard Ledger — Definition

**Filed:** 2026-10-06 (defined in conversation at GFED's request)
**Status:** CONCEPT — standing definition, not yet instantiated as a ledger file

---

The single canonical record of every storyboard scene/shot in a project: what has been approved, what is draft, and what is superseded — so nothing drifts or gets rebuilt twice.

A storyboard file is a working artifact; the ledger is the authority record behind it.

**Ledger row fields (per panel/shot):**
- Panel ID (e.g., SC-04 / P-01) — primary key, sourced from the script-to-storyboard decomposition
- Description (visual/action beat)
- Source file (which storyboard artifact the panel lives in)
- Version number
- Status: DRAFT / STAGED / LOCKED / SUPERSEDED
- Ruling date
- Ruling authority (who ruled it — GFED alone locks)

**Why it exists:** Without the ledger, each agent rebuilds from whatever artifact it found last — which is how characters drift, key art misses the chapter, or "verified" shots turn out to be a draft someone generated for exploration. The ledger is what keeps a LOCKed shot locked when six versions of a scene get iterated across sessions and agents.

**Precedents in GFED's system:** the same ledger pattern already runs for Threads (14-day format+topic ledger) and Root Access episode receipts — a ledger, not a folder of files.
