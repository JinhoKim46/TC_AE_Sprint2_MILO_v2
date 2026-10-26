# Hyperframes Composition Brief: MILO

## Objective
Create a short launch-style brag video for MILO.

## Output
- Composition directory: `docs/video/brag-output-2026-10-26-162310/composition/`
- Rendered video: `docs/video/brag-output-2026-10-26-162310/brag.mp4`, copied to `docs/video/milo-brag.mp4`
- Format: landscape — 1920x1080, 30 fps
- Duration: 40 s (by instruction; overrides the 15-25 s default)

## Source Material
- Project root: `sprint2/milo-v2`
- Primary files read: `src/milo/page.py` (chat UI, CSS tokens, labels), `src/milo/tools.py` (`_estimate_effect`,
  RANGE 0.8-1.2), `data/catalogue.yaml` (request-dispatch effect inputs: new minutes assumed 4),
  `data/demo_storylines.json` (the dispatch storyline), `data/kb/solutions/request-dispatch.md`, `data/kb/cases/C01.md`
- Product name: MILO
- Tagline / strongest claim: estimates the time an automation would save as a range, computed in code, not guessed
- Key UI moment to recreate: the chat composer and the answer card (range, sources, "What MILO did", stage boxes)
- Copy that must appear verbatim (from the project):
  - "We get about 40 service requests a week, and each takes about 12 minutes to assign. What could a shared queue save us?"
  - "MILO is reading your question, finding passages and checking the numbers"
  - "Sources for this answer", "Service area: Request and dispatch", "Past case: Duplicate dispatch across contact channels"
  - "What MILO did", "Searched the knowledge base", "Saved something you told me", "Calculated the time saving", "Done"
  - "Read the conversation", "Found passages", "Used tools", "Wrote the answer"
  - "Not enough information in the knowledge base."
- Computed numbers (from `tools.py`): 40 × (12 − 4) / 60 = 5.33 central; range 4.27 to 6.4 hours per week

## Creative Direction
- Tone preset: polished
- Creative direction: quiet product film on warm paper; the product's own UI is the hero
- Interpretation: six scenes at 5-8 s, long holds, blur swaps on one stage, no aggressive type
- Angle: one real owner question followed through the real UI; the product's honesty habits are the brag
- Hook: "40 service requests a week." / "12 minutes each to assign."
- Outro / punchline: "MILO" / "A diagnosis assistant for small service businesses."
- Avoid: generic SaaS language, abstract filler visuals, prices or money figures, real company names

## Visual Identity
- Background: #F5F4EF; card #FFFFFF; line #E2DFD6; step #EFEDE6
- Text: #1F1E1B; muted #6B6860
- Accent: #2F6B5E; accent soft #E7F0EC; notice #8A2F2F on #F8E6E6
- Display font: EB Garamond (bundled)
- Body font: Inter (bundled stand-in for the product's system-ui)
- UI scaled about 1.7x for 1080p legibility

## Storyboard
Use the storyboard in `brag-plan.md` as the creative contract.

1. Hook — 6.0 s — the owner's two numbers
2. The question — 7.0 s — typed into the composer, sent, working line
3. The range — 8.0 s — 4.27 to 6.4 hours per week, calculation and assumption
4. Sources and the saved fact — 8.0 s — two sources, three Done steps
5. Every step — 5.0 s — the four stage boxes
6. Honest, then the name — 6.0 s — the "not enough information" notice, then MILO

## Audio
- Audio role: sparse professional accents
- Audio arc: silent hook, tactile typing, soft payoffs, one hit on the name
- Music: none (disabled by instruction)
- Music cue guidance: unavailable
- Audio-reactive treatment: none
- Audio-coupled moments: typing (keypress set), Send click (`interface/click_003`), range landing
  (`impact/impactSoft_medium_001`), Done steps (`interface/bong_001`), final name (`impact/impactSoft_medium_004`)
- SFX analysis guidance: `<skill-dir>/assets/sfx/sfx-analysis.md`; low HF risk only
- Audio files: copied into `composition/assets/sfx/`

## Hyperframes Instructions
Root `index.html` mounts one sub-composition per scene from `compositions/`; SFX are root `<audio>` clips with ids.
`check` is the gate; no SPEC.md, storylines, usage, history, feedback or REVIEW.md. Render locally.

## Revision 2
See "Revision 2" in `brag-plan.md`: six scenes, landing-page palette, copy and call to action, one grid and one easing
family. Render ran with `render --docker` because the host has no ffprobe.
