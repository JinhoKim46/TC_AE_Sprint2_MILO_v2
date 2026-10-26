"""Add a spoken narration to the demo recording, timed to the captions.

Each caption in the recording's timeline (written by docs/video/demo-recording/record-demo.mjs) starts one narration
line. Lines are synthesised with Piper (a local neural voice; the default is the public-domain LJSpeech voice), placed
at their caption's time, mixed with ffmpeg, and muxed into a copy of the video. The video stream is copied, not re-encoded.

Run: uv run python scripts/narrate_demo.py --video <mp4> --timeline <json> --ffmpeg <ffmpeg>
     --voice data/voices/en_US-ljspeech-medium.onnx --out <mp4>
"""

from __future__ import annotations

import argparse
import json
import subprocess
import tempfile
import wave
from pathlib import Path

from piper import PiperVoice
from piper.config import SynthesisConfig

ROOT = Path(__file__).resolve().parents[1]


def synth(voice: PiperVoice, text: str, path: Path, window: float) -> float:
    """Speak one line into a WAV file. If the line is longer than its window, it is spoken a little faster."""
    scale = 1.0
    for _ in range(3):
        with wave.open(str(path), "wb") as w:
            voice.synthesize_wav(
                text, w, syn_config=SynthesisConfig(length_scale=scale)
            )
        with wave.open(str(path), "rb") as w:
            seconds = w.getnframes() / w.getframerate()
        if seconds <= window - 0.2:
            break
        scale = min(1.6, scale * seconds / (window - 0.2))
    return seconds


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", required=True, type=Path)
    ap.add_argument("--timeline", required=True, type=Path)
    ap.add_argument(
        "--narration",
        type=Path,
        default=ROOT / "docs/video/demo-recording/narration.json",
    )
    ap.add_argument(
        "--voice", type=Path, default=ROOT / "data/voices/en_US-ljspeech-medium.onnx"
    )
    ap.add_argument("--ffmpeg", default="ffmpeg")
    ap.add_argument("--out", required=True, type=Path)
    args = ap.parse_args()

    lines = json.loads(args.narration.read_text())
    timeline = json.loads(args.timeline.read_text())
    voice = PiperVoice.load(str(args.voice))
    workdir = Path(tempfile.mkdtemp(prefix="narration-"))
    clips = []
    for i, cap in enumerate(timeline):
        text = lines.get(cap["text"])
        if not text:  # an empty line means the caption is covered by the one before it
            continue
        nxt = timeline[i + 1]["at"] if i + 1 < len(timeline) else cap["at"] + 8.0
        path = workdir / f"line{i:02d}.wav"
        seconds = synth(voice, text, path, nxt - cap["at"])
        clips.append((cap["at"], path, seconds, text))
    filters, inputs = [], []
    for n, (at, path, seconds, text) in enumerate(clips):
        inputs += ["-i", str(path)]
        ms = int(at * 1000)
        filters.append(f"[{n}:a]adelay={ms}|{ms},volume=1.0[a{n}]")
    mix = "".join(f"[a{n}]" for n in range(len(clips)))
    filters.append(f"{mix}amix=inputs={len(clips)}:normalize=0[aout]")
    total = timeline[-1]["at"] + 10.0  # a fixed length: a padded mix would never end
    narration = workdir / "narration.wav"
    subprocess.run(
        [
            args.ffmpeg,
            "-y",
            "-loglevel",
            "error",
            *inputs,
            "-filter_complex",
            ";".join(filters),
            "-map",
            "[aout]",
            "-t",
            f"{total:.2f}",
            "-ac",
            "2",
            "-ar",
            "44100",
            str(narration),
        ],
        check=True,
    )
    subprocess.run(
        [
            args.ffmpeg,
            "-y",
            "-loglevel",
            "error",
            "-i",
            str(args.video),
            "-i",
            str(narration),
            "-map",
            "0:v",
            "-map",
            "1:a",
            "-c:v",
            "copy",
            "-c:a",
            "aac",
            "-b:a",
            "160k",
            "-shortest",
            str(args.out),
        ],
        check=True,
    )
    for at, path, seconds, text in clips:
        print(f"{at:6.2f}s  {seconds:5.2f}s  {text}")
    print("wrote", args.out)


if __name__ == "__main__":
    main()
