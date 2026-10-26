# Automated screen recording of the MILO chat

Made by a browser script, not by a person at a screen. It drives Chrome (puppeteer-core), records the page with
`page.screencast`, and adds a caption line at the bottom. The answers come from the live model, so the run costs a few
cents.

Steps: landing page, sign-in, a question, the tool steps, the full-source viewer with the passage highlighted, a fact
recorded by a tool call, a destructive action waiting for approval, and the summary with the proposed spec.

Run (after starting the demo server with `MILO_LIVE=1 MILO_DEMO_PASSWORD=<pick> uv run python scripts/demo_server.py`):

    node record-demo.mjs http://127.0.0.1:5057 <the password> milo-chat-demo.mp4 <path to an ffmpeg binary>

`record-demo.mjs` imports `puppeteer-core`, so install it in a folder of your own first. The recording is
`milo-chat-demo.mp4` in this folder.

Known issue (open): the recording's length does not match the real session. The last run shows about 55 seconds of
video for a session that takes longer in real time, so the clock is compressed. Narration cannot be timed to scenes
until this is fixed. Check the frame timestamps from Chrome's screencast against wall-clock times at each caption.
