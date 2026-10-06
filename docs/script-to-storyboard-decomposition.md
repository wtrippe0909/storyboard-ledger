# Script-to-Storyboard Decomposition (Reference)

**Source:** Collaborator (Meta AI) explainer, relayed via GFED, 2026-10-06
**Status:** REFERENCE / INFORMATION — production standards, no canon claims
**Relation:** This is the input layer for the Master Storyboard Ledger concept (the ledger is the canonical record; this decomposition is the feed that populates it).

---

**TL;DR:** In storyboard creation, the script writer translates narrative prose into discrete, visually executable beats — the structural bridge between text and imagery, defining shot boundaries, blocking, timing, and focal points so the storyboard artist or visual pipeline can render each frame without ambiguity.

**Core Function in Storyboarding**

A standard screenplay describes scenes; a storyboard requires shots. The writer's role pivots from broad narrative drafting to technical visual decomposition:
- Deconstructing Action into Panels: Breaking continuous action lines (e.g., "He dodges the blast and scrambles up the fire escape") into sequential panels: Setup → Impact → Reaction → Recovery.
- Providing Technical Shot Metadata: Attaching camera framing (Wide, Medium, Close-Up), angle (Low, High, Dutch), and movement prompts (Pan, Tilt, Push-In) to each narrative beat.
- Syncing Audio to Visual Beats: Aligning dialogue snippets, voiceover, SFX, and musical cues directly to corresponding panel numbers.
- Guiding Spatial Continuity (Blocking): Enforcing the 180-degree rule, screen direction, and spatial orientation in panel notes.

**Script-to-Storyboard Data Structure**

| Field | Source Script Element | Storyboard Translation | Example |
|---|---|---|---|
| Scene / Panel ID | Scene Heading / Action line | Unique sequence identifier | SC-04 / P-01 |
| Shot Type & Angle | Visual cue in action text | Specific framing constraint | MCU (Medium Close-Up), Low Angle |
| Visual / Action | Action paragraph | Concrete physical description of what is drawn | "Marcus turns sharply toward the alley entrance, gun raised." |
| Camera Movement | Implied camera focus | Direct mechanical camera instructions | Handheld; rapid push-in on Marcus's eyes |
| Audio / Dialogue | Character speech / SFX line | Exact sync point | SFX: Distant siren. VO: "I knew the clock was running." |
| Duration / Timing | Pacing & rhythm | Frame hold or estimated seconds | 1.5 sec |

**Operational Workflow: From Script to Locked Boards**
- Beat Breakdown: Writer marks up the script into distinct visual moments (each beat requiring a camera change or major subject shift).
- Shot List Generation: Writer drafts the shot list — establishing shots, coverage angles, insert shots, transitions.
- Roughs / Thumbnails Pass: Writer collaborates with director and storyboard artist during rough thumbnail sketching to align narrative intent and focal points with the script's emotional beat.
- Panel Revision & Trimming: If a board reveals a dragging or redundant sequence, the writer cuts redundant dialogue or condenses action beats before final panels.

**Ledger integration note (Muse):** When the Master Storyboard Ledger is built, the Scene/Panel ID from this structure becomes the ledger's primary key — one ledger row per panel, carrying status (DRAFT / STAGED / LOCKED / SUPERSEDED), ruling date, and ruling authority. That is what prevents drift across sessions and agents.
