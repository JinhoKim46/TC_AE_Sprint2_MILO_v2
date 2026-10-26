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

import numpy as np
from piper import PiperVoice
from piper.config import SynthesisConfig

ROOT = Path(__file__).resolve().parents[1]


# A calmer delivery: a slower pace, and less variation in pitch and rhythm than the defaults.
CALM = {"noise_scale": 0.45, "noise_w_scale": 0.5}


def synth(voice: PiperVoice, text: str, path: Path, window: float) -> float:
    """Speak one line into a WAV file. Calm by default; only a line longer than its window is spoken a little faster."""
    scale = 1.1
    for _ in range(4):
        with wave.open(str(path), "wb") as w:
            voice.synthesize_wav(
                text, w, syn_config=SynthesisConfig(length_scale=scale, **CALM)
            )
        with wave.open(str(path), "rb") as w:
            seconds = w.getnframes() / w.getframerate()
        if seconds <= window - 0.2:
            break
        # Piper: a larger length_scale is slower, so a line that is too long gets a smaller one (faster).
        scale = max(0.75, scale * (window - 0.2) / seconds)
    return seconds


def background(seconds: float, rate: int = 44100) -> np.ndarray:
    """A light, bright background: a major-key progression (C, G, Am, F) with plucked eighth notes. Quiet by design."""
    n = int(seconds * rate)
    t = np.arange(n) / rate
    beat = 60 / 104
    chords = [
        (523.25, 659.25, 783.99),
        (392.0, 493.88, 587.33),
        (440.0, 523.25, 659.25),
        (349.23, 440.0, 523.25),
    ]
    out = np.zeros(n)

    def pluck(freq: float, start: float, length: float, level: float) -> None:
        i = int(start * rate)
        k = np.arange(int(length * rate)) / rate
        env = np.exp(-k * 7.0) * np.minimum(1, k / 0.004)
        sig = (
            (np.sin(2 * np.pi * freq * k) + 0.2 * np.sin(4 * np.pi * freq * k))
            * env
            * level
        )
        j = min(n, i + len(sig))
        if j > i:
            out[i:j] += sig[: j - i]

    bar = 4 * beat
    for b in range(int(seconds / bar) + 1):
        chord = chords[b % 4]
        for k in range(8):  # eighth notes, climbing and falling through the chord
            freq = chord[[0, 1, 2, 1][k % 4]] * (2 if k >= 4 else 1)
            pluck(freq, b * bar + k * beat / 2, 0.9, 0.35)
    out = out * np.minimum(1, t / 2.0) * np.minimum(1, (seconds - t) / 3.0)
    out = out / max(1e-9, float(np.max(np.abs(out)))) * 0.5
    return np.stack([out, out], axis=1)


def mix_with_background(narration: Path, out: Path, gain: float = 0.12) -> None:
    """Lay the quiet background under the spoken narration and write one stereo WAV."""
    with wave.open(str(narration), "rb") as w:
        rate, channels = w.getframerate(), w.getnchannels()
        voice = (
            np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).reshape(
                -1, channels
            )
            / 32768
        )
    bed = background(len(voice) / rate, rate) * gain
    mixed = np.clip(
        voice * 0.8 + bed[: len(voice)], -0.95, 0.95
    )  # headroom: no clipping
    with wave.open(str(out), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(rate)
        w.writeframes((mixed * 32767).astype(np.int16).tobytes())


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
    bed_mix = workdir / "narration-with-music.wav"
    mix_with_background(narration, bed_mix)
    subprocess.run(
        [
            args.ffmpeg,
            "-y",
            "-loglevel",
            "error",
            "-i",
            str(args.video),
            "-i",
            str(bed_mix),
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
