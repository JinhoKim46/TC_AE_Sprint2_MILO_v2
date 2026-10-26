# Automated screen recording of the MILO chat

Made by a browser script, not by a person at a screen. The script starts Chrome on a virtual display (Xvfb), grabs that
display in real time with ffmpeg, and writes a caption line at the bottom of the picture. The answers come from the
live model, so a run costs a few cents. Only the virtual display is captured; the real desktop is never recorded.

## Steps

1. Get Xvfb (`sudo apt install xvfb`, or unpack the package into a folder of your own without root).
2. Start the virtual display: `Xvfb :99 -screen 0 1440x900x24 -nolisten tcp &`
3. Start the demo server with the live model:
   `MILO_LIVE=1 MILO_DEMO_PASSWORD=<pick one> uv run python scripts/demo_server.py` (port 5057).
4. Record (install `puppeteer-core` in a folder of your own first):
   `RECORD_DISPLAY=:99 node record-demo.mjs http://127.0.0.1:5057 <the password> milo-chat-demo.mp4 <path to an ffmpeg binary>`

## What the recording shows

Landing page, sign-in, a question with the live answer and its sources, the tool steps, the full-source viewer with the
passage highlighted, a fact recorded by a tool call, a destructive action waiting for approval, and the summary with
the proposed spec. The run lasts about 51 seconds, real time.

The browser shows the notice "Chrome is being controlled by automated test software". It is left in on purpose: it is
the honest sign that the recording was automated.

## Narration

`record-demo.mjs` also writes `caption-timeline.json`: the time each caption appeared. `narration.json` gives one spoken line
per caption (an empty line means the caption is covered by the one before). Then:

    uv run python scripts/narrate_demo.py --video milo-chat-demo.mp4 --timeline caption-timeline.json \
        --ffmpeg <ffmpeg> --out milo-chat-demo-narrated.mp4

The narration is calm: a slower pace and less variation than the defaults. A quiet, bright background (a major-key figure) runs under it, about 18 dB below the voice. The voice is Piper with the public-domain LJSpeech model (`data/voices/en_US-ljspeech-medium.onnx`, not in git; download
it from the rhasspy/piper-voices repository). Each line starts at its caption's time, and is spoken faster only if it is
longer than its scene. The video is copied, not re-encoded.

## Earlier versions

Two earlier methods gave a video whose length did not match the session (a timed screencast and a screenshot loop).
They are replaced by the real-time grab above.
