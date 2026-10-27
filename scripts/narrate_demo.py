"""Narrate the demo recording: spoken lines, matching subtitles, and a quiet background, all timed to the screen.

The recording (no on-screen captions) comes with a timeline of scene starts (docs/video/demo-recording/record-demo.mjs).
narration.json gives one spoken line per scene; an empty line means the scene continues the one before it.

For each line:
- Piper speaks it with a calm delivery, starting at its scene's time.
- The subtitle is the same sentence, shown from the moment its speech starts to the moment it ends, so the words and the
  subtitle match and stay in sync.
- The subtitle sits at the top centre on a semi-transparent dark box, with white text.

Then a quiet major-key background runs under the speech, and the subtitles are burnt into the picture with ffmpeg.

Run: uv run python scripts/narrate_demo.py --video <mp4> --timeline <json> --ffmpeg <ffmpeg> --out <mp4>
"""

from __future__ import annotations

import argparse
import itertools
import json
import subprocess
import tempfile
import textwrap
import wave
from pathlib import Path

import numpy as np
from piper import PiperVoice
from piper.config import SynthesisConfig

ROOT = Path(__file__).resolve().parents[1]
# A calmer delivery: a slower pace, and less variation in pitch and rhythm than the defaults.
CALM = {"noise_scale": 0.45, "noise_w_scale": 0.5}
SUBTITLE_STYLE = "Style: Default,Sans,28,&H00FFFFFF,&H000000FF,&H00000000,&H66000000,0,0,0,0,100,100,0,0,3,8,0,8,80,80,40,1"  # white text; opaque box at 60% opacity (ASS alpha 00 is opaque); top centre (alignment 8)


def synth(voice: PiperVoice, text: str, path: Path, window: float) -> float:
    """Speak one line into a WAV file. Calm by default; only a line longer than its window is spoken a little faster."""
    scale = 1.1
    seconds = 0.0
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


def mix_speech_and_background(speech: Path, out: Path, gain: float = 0.12) -> None:
    """The speech at a steady level, the quiet background under it, one stereo WAV with headroom against clipping."""
    with wave.open(str(speech), "rb") as w:
        rate, channels = w.getframerate(), w.getnchannels()
        voice = (
            np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).reshape(
                -1, channels
            )
            / 32768
        )
    bed = background(len(voice) / rate, rate) * gain
    mixed = np.clip(voice * 0.8 + bed[: len(voice)], -0.95, 0.95)
    with wave.open(str(out), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(rate)
        w.writeframes((mixed * 32767).astype(np.int16).tobytes())


def ass_time(seconds: float) -> str:
    h, rest = divmod(seconds, 3600)
    m, s = divmod(rest, 60)
    return f"{int(h)}:{int(m):02d}:{s:05.2f}"


def write_subtitles(cues: list[tuple[float, float, str]], path: Path) -> None:
    """ASS subtitles: each cue is shown from the start of its speech to the end of it."""
    header = (
        "[Script Info]\nScriptType: v4.00+\nPlayResX: 1440\nPlayResY: 900\nWrapStyle: 0\nScaledBorderAndShadow: yes\n\n"
        "[V4+ Styles]\n"
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, "
        "Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, "
        "MarginV, Encoding\n"
        f"{SUBTITLE_STYLE}\n\n"
        "[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"
    )
    events = []
    for start, end, text in cues:
        wrapped = r"\N".join(textwrap.wrap(text, width=72))
        events.append(
            f"Dialogue: 0,{ass_time(start)},{ass_time(end)},Default,,0,0,0,,{wrapped}"
        )
    path.write_text(header + "\n".join(events) + "\n", encoding="utf-8")


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
    ap.add_argument(
        "--subtitles",
        action="store_true",
        help="also burn the narration as subtitles (off by default)",
    )
    args = ap.parse_args()

    lines = json.loads(args.narration.read_text())
    timeline = json.loads(args.timeline.read_text())
    voice = PiperVoice.load(str(args.voice))
    workdir = Path(tempfile.mkdtemp(prefix="narration-"))

    clips: list[tuple[float, Path, float, str]] = []
    for i, cap in enumerate(timeline):
        text = lines.get(cap["text"])
        if not text:  # an empty line: this scene continues the one before it
            continue
        nxt = timeline[i + 1]["at"] if i + 1 < len(timeline) else cap["at"] + 8.0
        path = workdir / f"line{i:02d}.wav"
        seconds = synth(voice, text, path, nxt - cap["at"])
        clips.append((cap["at"], path, seconds, text))

    # Place every line at its scene's time, and check that no line runs into the next one.
    filters, inputs = [], []
    for n, (at, path, _seconds, _text) in enumerate(clips):
        inputs += ["-i", str(path)]
        ms = int(at * 1000)
        filters.append(f"[{n}:a]adelay={ms}|{ms}[a{n}]")
    filters.append(
        "".join(f"[a{n}]" for n in range(len(clips)))
        + f"amix=inputs={len(clips)}:normalize=0[speech]"
    )
    speech = workdir / "speech.wav"
    total = timeline[-1]["at"] + 10.0
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
            "[speech]",
            "-t",
            f"{total:.2f}",
            "-ac",
            "2",
            "-ar",
            "44100",
            str(speech),
        ],
        check=True,
    )
    mixed = workdir / "speech-with-background.wav"
    mix_speech_and_background(speech, mixed)

    cues = [(at, at + seconds, text) for at, _path, seconds, text in clips]
    for (a, a_end, _), (b, _, _) in itertools.pairwise(cues):
        if a_end > b + 0.05:
            print(
                f"warning: a line starting at {a:.2f}s runs past the next scene at {b:.2f}s"
            )
    subs = workdir / "subtitles.ass"
    write_subtitles(cues, subs)

    if args.subtitles:
        # Burn the subtitles into the picture and add the mixed audio. The picture is encoded once here.
        subprocess.run(
            [
                args.ffmpeg,
                "-y",
                "-loglevel",
                "error",
                "-i",
                str(args.video),
                "-i",
                str(mixed),
                "-filter_complex",
                f"[0:v]ass={subs}[v]",
                "-map",
                "[v]",
                "-map",
                "1:a",
                "-c:v",
                "libx264",
                "-preset",
                "medium",
                "-crf",
                "20",
                "-pix_fmt",
                "yuv420p",
                "-c:a",
                "aac",
                "-b:a",
                "160k",
                "-shortest",
                str(args.out),
            ],
            check=True,
        )
    else:
        # Narration only: the picture is copied as it is, and the mixed audio is added.
        subprocess.run(
            [
                args.ffmpeg,
                "-y",
                "-loglevel",
                "error",
                "-i",
                str(args.video),
                "-i",
                str(mixed),
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
    for at, _path, seconds, text in clips:
        print(f"{at:6.2f}s  {seconds:5.2f}s  {text}")
    print("wrote", args.out)


if __name__ == "__main__":
    main()
