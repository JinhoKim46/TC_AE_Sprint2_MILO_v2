# Brag Plan: MILO

Run notes (deviations by instruction):
- Full /brag workflow, not brag-slim, by the caller's explicit request.
- Duration is 40 s by instruction (`--duration 40`, allowed 30-50 s). This overrides the skill's 15-25 s law.
- Music off and narration off by instruction. SFX stay on (skill default), sparse and low high-frequency risk.
  Music-dependent items (cue preset, beat locks, beat grid, audio-reactive treatment) are skipped because there is no music.
- All data in the video is fictional. No real company, person or price appears. The recreated chat UI omits the
  "Session cost" line so no money figure is on screen.

## What is this app?
MILO is a diagnosis assistant for small service businesses that run maintenance, printers and office equipment: the
owner describes one kind of work, and MILO finds matching passages, cites them, records the owner's facts, estimates
the time an automation would save as a range computed in code, and shows each step it took.

## The angle
Quiet confidence: one real question, answered honestly. The video follows a single owner question from the product's
own demo storyline (40 requests a week, 12 minutes each to assign) through the real chat UI, and lets the product's
habits do the bragging: a range instead of a guess, sources instead of assertions, a saved fact, a visible path, and a
plain "not enough information" when the knowledge base has nothing.

## Hook (first 2-3 seconds)
The owner's numbers, set large on the product's warm paper ground: "40 service requests a week." then
"12 minutes each to assign." The numbers are the hook because the whole video answers them.

## Key moments (the middle)
- The owner's question types into MILO's real composer ("Describe one kind of work in your business, or ask a question")
  and lands as the green user bubble; the working line reads "MILO is reading your question, finding passages and
  checking the numbers".
- The answer arrives as a range: 4.27 to 6.4 hours per week, counted up, with the calculation and the assumption
  shown (new minutes assumed 4, from the catalogue). Caption: computed in code, not guessed.
- "Sources for this answer": [1] Service area: Request and dispatch, [2] Past case: Duplicate dispatch across contact
  channels. Then "What MILO did": Searched the knowledge base, Saved something you told me, Calculated the time
  saving, each marked Done.
- The four stage boxes: Read the conversation / Found passages / Used tools / Wrote the answer.

## Outro / punchline
The product's own refusal notice, "Not enough information in the knowledge base.", framed as a virtue; then "MILO" and
the one-line description. Silence apart from one soft hit.

## User flow worth showing
Owner types the dispatch question -> MILO works (reading, finding passages, checking numbers) -> the answer card with a
computed range, cited sources, the saved fact and the steps.

## Tone
- Preset: polished
- Creative direction: quiet product film on warm paper; the product's own UI is the hero
- Interpretation: few scenes, long holds, soft blur swaps on one stage, no aggressive type, every line held long
  enough to read.

## Format: landscape — 1920x1080
## Duration: 40 s

## Visual identity (from the project, `src/milo/page.py` `_BASE_CSS`)
- Background: #F5F4EF
- Card: #FFFFFF, line #E2DFD6, step #EFEDE6
- Accent: #2F6B5E (accent soft #E7F0EC)
- Text: #1F1E1B (muted #6B6860)
- Notice (low): #8A2F2F on #F8E6E6
- Display font: EB Garamond (video choice for the hook and outro titles; bundled)
- Body font: Inter (the product uses system-ui; Inter is the bundled stand-in)
- Strongest visual element: the answer card with its stage boxes, sources list and "What MILO did" checklist

## Share copy (draft)
MILO: a diagnosis assistant for small service businesses. Tell it about 40 requests a week at 12 minutes each, and it
answers with a computed range, its sources and every step it took.

## Audio direction
- Role: sparse professional accents
- Music: none (disabled by instruction)
- Music treatment: none
- Music cue guidance: unavailable (music off)
- Audio-reactive treatment: none (no music)
- SFX posture: sparse, motion-matched, low high-frequency risk
- Audio-coupled moments: key ticks while the question types; a click on Send; a soft hit when the range lands; a light
  accent per "Done" step; a soft hit under the final name
- Restraint rule: no sound on every caption; nothing bright or repeated fast

## Storyboard

### Scene 1 — Hook — 6.0 s
Paper ground. "40 service requests a week." blurs in word by word, then "12 minutes each to assign." beneath it.
Small muted line: "Where does that time go?" Numbers 40 and 12 in the accent colour.
Sequential/interaction: yes — two lines arrive one after another, each held at least 2 s.
Audio intent: quiet start. Audio-coupled idea: none.
Transition mood: soft → Scene 2

### Scene 2 — The question — 7.0 s
Recreated MILO chat: sidebar ("How MILO works" four steps), top bar "Diagnosis chat", composer. The question types in:
"We get about 40 service requests a week, and each takes about 12 minutes to assign. What could a shared queue save us?"
Send is pressed; the green user bubble appears; the working line with three dots.
Sequential/interaction: yes — typing, then a simulated click on Send.
Audio intent: tactile. Audio-coupled idea: key ticks while typing, click on Send.
Transition mood: soft → Scene 3

### Scene 3 — The range — 8.0 s
Answer card, scaled up: "Calculated the time saving". The range counts up to "4.27 – 6.4 hours per week". Beneath:
"40 requests × (12 − 4) minutes ÷ 60 = 5.33 central, ±20%" and the assumption label "new minutes assumed 4: minutes of
staff time per request with one shared queue". Caption: "A range, computed in code. Not guessed."
Sequential/interaction: yes — count-up, then calculation line, then caption (held ≥2 s).
Audio intent: the payoff. Audio-coupled idea: soft hit on the range landing.
Transition mood: soft → Scene 4

### Scene 4 — Sources and the saved fact — 8.0 s
Left: "Sources for this answer", two source cards arrive one by one. Right: "What MILO did", three checklist rows arrive
one by one, each with a "Done" pill; the saved-fact row shows the owner's numbers (requests per week 40, minutes to
assign 12). Caption: "Cites where it came from. Records what you said."
Sequential/interaction: yes — 2 source cards then 3 step rows, ~0.5 s apart, full set held ≥3 s.
Audio intent: orderly. Audio-coupled idea: light accent per step row.
Transition mood: soft → Scene 5

### Scene 5 — Every step — 5.0 s
The four stage boxes from the answer card: Read the conversation (New, first message), Found passages (2, from 2
documents), Used tools (3, steps taken), Wrote the answer (1, from the passages). Caption: "Shows each step it took."
Sequential/interaction: yes — boxes arrive left to right, held ≥2.5 s.
Audio intent: calm. Audio-coupled idea: none.
Transition mood: soft → Scene 6

### Scene 6 — Honest, then the name — 6.0 s
The product's notice: "Not enough information in the knowledge base." Caption: "And it says when it does not know."
Then a swap to "MILO" in large type and "A diagnosis assistant for small service businesses." held to the end (≥2.5 s).
Sequential/interaction: none.
Audio intent: resolve. Audio-coupled idea: one soft hit on the name.

**Music mood for this video:** none (disabled)
**Audio summary:** near-silent film with tactile UI sounds during the question and a few soft accents on the payoffs.

## Revision 2 (coordinator quality requirements, supersedes the storyboard above)

Palette from `src/milo/landing.py`: ground #F5F4EF, ink #1F1E1B, accent #2C6B5C, soft accent #E6F0EC, warning #8A5418
(warning soft #FBF1DF), muted #67645B. Display face EB Garamond, body face Inter; roles: title 76 px, card title 36 px,
body 32 px, caption 28 px. One grid: 160 px side margins, 112 px top and bottom. Entrances power3.out (fade + 24 px
rise), crossfades power2.inOut 0.6 s between overlapping scenes, no overshoot. Mascot and mark from `src/milo/static/`.

1. Title card, 0-6 s (centred): mascot, "MILO", "A diagnosis assistant for small service businesses."
2. How it works, 6-14 s: the four steps from the landing page (describe; finds passages with numbered sources; checks
   and records, savings computed in code as a range; answers with every step shown).
3. Sample exchange, 14-20.5 s: the owner's question types into the chat composer and is sent.
4. Sample exchange, 20.5-28.5 s: the question, the landing page's sample answer with citation [1], the sources, and the
   estimate panel 4.3-6.4 hours a week with its labelled assumption (4 minutes per request with one shared queue).
5. Transparency, 28.5-34 s: stage boxes, "Sources for this answer" [1] [2], and the tool steps marked Done.
6. End card, 34-40 s (centred): "See how one answer is made", the landing page line, and the "Open the chat" button.
