# Production Storyboard Script / Shot List — Working Template

**Source:** Collaborator (Meta AI), relayed via GFED, 2026-10-06
**Status:** REFERENCE / WORKING TEMPLATE — production standards, no canon claims
**Relation:** The fill-in form whose completed rows feed the Master Storyboard Ledger. Panel ID is the shared key: one template row → one ledger row.

---

## 1. Project & Scene Metadata

PROJECT NAME:      [Project Title]
EPISODE / SEGMENT: [Ep. Number / Name / Ad Spot ID]
SCENE NUMBER:      [Scene ID]
LOCATION / TIME:   [INT. / EXT. - LOCATION NAME - DAY / NIGHT]
TARGET ASPECT RATIO:[16:9 / 2.39:1 / 9:16 / 4:3]
WRITER / DIRECTOR: [Name]
STORYBOARD ARTIST: [Name]
VERSION / STATUS:  [v1.0 - Draft / In Review / Locked]
ESTIMATED RUNTIME: [MM:SS]

## 2. Technical Notation & Camera Key

Standardized abbreviations used across panels:

**Framing / Shot Size:**
- ELS / VWS: Extreme Long Shot / Very Wide Shot
- WS: Wide Shot / Establishing Shot
- FS: Full Shot (entire character head-to-toe)
- MS: Medium Shot (waist up)
- MCU: Medium Close-Up (chest up)
- CU: Close-Up (face/head)
- ECU: Extreme Close-Up (eyes, hands, detail item)
- OTS: Over-the-Shoulder
- POV: Point-of-View Shot

**Camera Angle & Height:**
- EYE: Eye Level
- LOW: Low Angle (looking up)
- HIGH: High Angle (looking down)
- DUTCH: Dutch Angle (canted/tilted horizon)
- BIRD: Bird's Eye View (top-down 90°)
- WORM: Worm's Eye View (ground-level looking up)

**Camera Movement:**
- STATIC: Locked-off tripod
- PAN [L/R]: Horizontal pivot (left or right)
- TILT [U/D]: Vertical pivot (up or down)
- DOLLY [IN/OUT]: Camera physically moving toward or away from subject
- TRACK / TRUCK [L/R]: Camera physically moving lateral to subject
- BOOM / CRANE [U/D]: Vertical pedestal/crane movement
- HANDHELD: Organic/shaky camera movement
- ZOOM [IN/OUT]: Optical focal length change
- WHIP [DIR]: Rapid whip pan

## 3. Blank Storyboard Shot-List Template

### SCENE [XX]: [INT./EXT. LOCATION - DAY/NIGHT]
**Scene Objective:** [One-sentence emotional or narrative goal of this sequence]
**Key Continuity Notes:** [Character placement, screen direction (e.g., A moves Screen Left to Screen Right), lighting tone]

| Panel ID | Framing & Angle | Movement | Visual Action & Blocking | Audio (Dialogue, VO, SFX, Score) | Duration | Transition |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **P-01** | `[SHOT TYPE]`<br>`[ANGLE]` | `[CAMERA MOVE]` | **Subject:** [Character/Object]<br>**Action:** [Visible physical action & posture]<br>**Focal Point:** [Where eye looks in frame] | **[SPEAKER]:** "[Dialogue line]"<br>**SFX:** [Sound effects]<br>**MUSIC:** [Score cue] | `0.0s` | `CUT` |
| **P-02** | `[SHOT TYPE]`<br>`[ANGLE]` | `[CAMERA MOVE]` | **Subject:** [Character/Object]<br>**Action:** [Continuation or reaction beat]<br>**Focal Point:** [Where eye looks in frame] | **[SPEAKER]:** "[Dialogue line]"<br>**SFX:** [Sound effects]<br>**MUSIC:** [Score cue] | `0.0s` | `CUT` |
| **P-03** | `[SHOT TYPE]`<br>`[ANGLE]` | `[CAMERA MOVE]` | **Subject:** [Character/Object]<br>**Action:** [Climactic beat / insert beat]<br>**Focal Point:** [Where eye looks in frame] | **[SPEAKER]:** "[Dialogue line]"<br>**SFX:** [Sound effects]<br>**MUSIC:** [Score cue] | `0.0s` | `CUT / DISSOLVE` |

## 4. Worked Production Example

SCENE 04: INT. ARCHIVE VAULT - NIGHT
- Scene Objective: Marcus breaches the terminal room and discovers the server drive has already been extracted.
- Continuity Notes: Low key amber/blue emergency lighting. Marcus enters screen left, advances toward screen right.

| Panel ID | Framing & Angle | Movement | Visual Action & Blocking | Audio (Dialogue, VO, SFX, Score) | Duration | Transition |
|---|---|---|---|---|---|---|
| SC04-P01 | WS / Eye Level | DOLLY IN (Slow) | **Subject:** MARCUS (40s, tactical gear). **Action:** Heavy vault door slides open slowly. Marcus steps across the threshold, flashlight beam cutting through airborne dust. **Focal Point:** Center frame (Marcus's silhouette against hall light). | **SFX:** Heavy pneumatic hiss of door seals breaking. Faint industrial hum. **MUSIC:** Low-register sub-bass drone begins. | 3.0s | CUT |
| SC04-P02 | MS / Low Angle | TRACK R | **Subject:** MARCUS. **Action:** Marcus advances along server rack row B. Flashlight scans upward. His weapon is lowered but ready. **Focal Point:** Right third of frame (leading the walk). | **SFX:** Combat boot treads over metal grating. **MARCUS (whisper):** "Clear. Rack two reached." | 2.0s | CUT |
| SC04-P03 | OTS (Over Marcus's shoulder) / Eye Level | STATIC | **Subject:** TERMINAL CONSOLE. **Action:** Flashlight illuminates Terminal 09. The primary hard-drive bay is open; cables hang severed and frayed. **Focal Point:** Center (gaping drive bay). | **SFX:** High-pitched capacitor whine. **MUSIC:** Drone drops out abruptly. | 1.5s | CUT |
| SC04-P04 | ECU / High Angle | PUSH IN (Fast) | **Subject:** DRIVE BAY PORT. **Action:** Fresh scorch marks around the SATA connectors. A drop of fresh grease glints on the rim. **Focal Point:** Severed wire bundle. | **SFX:** Spark sizzle (crackling static). | 1.0s | CUT |
| SC04-P05 | CU / Low Angle (Canted) | HANDHELD / JITTER | **Subject:** MARCUS. **Action:** Marcus freezes. Flashlight drops slightly. He turns his head sharply back toward the entry corridor behind him. **Focal Point:** Marcus's eyes (shifting left). | **MARCUS:** "Command... we're late." **SFX:** (Off-screen) Heavy metallic click of an assault rifle bolt cycling. | 2.5s | HARD CUT |

## Implementation Tips for Creative Operations & AI Pipelines

- **1-to-1 Prompt Mapping:** Each row directly corresponds to an AI image/video generation prompt. Combine Framing & Angle + Visual Action & Blocking for the positive prompt; Audio drives speech synthesis and Foley timing.
- **Screen Direction Consistency:** Enforce an explicit field for character facing (Looking Left-to-Right vs. Looking Right-to-Left) to prevent crossing the line of action across sequential panels.
- **Duration Summation:** Maintain the Duration column to calculate precise animatic timeline lengths before allocating time to illustration or 3D layout rendering.

**Ledger integration note (Muse):** The template's VERSION / STATUS field maps 1:1 to the ledger's status values (Draft → DRAFT, In Review → STAGED, Locked → LOCKED). When a shot list is filled in, each Panel ID row is copied into the ledger with its status, version, and ruling authority — the ledger becomes the cross-session memory; the template stays the per-scene working form.
