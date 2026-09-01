#!/usr/bin/env python3
"""Compose recorded slides, segmented narration, BGM, and ASS captions into MP4."""

from __future__ import annotations

import argparse
import json
import shlex
import shutil
import subprocess
from datetime import datetime
from pathlib import Path


def ass_filter_path(path: Path) -> str:
    value = str(path.resolve()).replace("\\", "\\\\").replace(":", "\\:").replace("'", "\\'")
    return f"ass='{value}'"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--visual", required=True, type=Path)
    parser.add_argument("--timing", required=True, type=Path)
    parser.add_argument("--bgm", required=True, type=Path)
    parser.add_argument("--subtitles", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--ffmpeg", default="ffmpeg")
    parser.add_argument("--backup-existing", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    manifest = json.loads(args.timing.read_text(encoding="utf-8"))
    segments = manifest.get("segments", [])
    if not segments:
        raise SystemExit("Timing manifest has no segments")

    for path in [args.visual, args.bgm, args.subtitles, *[Path(row["voice_file"]) for row in segments]]:
        if not path.exists():
            raise SystemExit(f"Missing input: {path}")

    if args.output.exists() and not (args.backup_existing or args.dry_run):
        raise SystemExit("Output exists. Use --backup-existing to preserve and replace it.")
    if args.output.exists() and args.backup_existing and not args.dry_run:
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        backup = args.output.with_name(f"{args.output.stem}.backup-{stamp}{args.output.suffix}")
        shutil.copy2(args.output, backup)

    command = [args.ffmpeg, "-y", "-i", str(args.visual)]
    for row in segments:
        command += ["-i", row["voice_file"]]
    command += ["-stream_loop", "-1", "-i", str(args.bgm)]

    filters = []
    voice_labels = []
    for input_index, row in enumerate(segments, start=1):
        delay_ms = int(round(float(row["voice_start"]) * 1000))
        label = f"v{input_index}"
        filters.append(f"[{input_index}:a]adelay={delay_ms}|{delay_ms}[{label}]")
        voice_labels.append(f"[{label}]")

    voice_mix = "".join(voice_labels)
    filters.append(
        f"{voice_mix}amix=inputs={len(voice_labels)}:duration=longest:normalize=0,"
        "loudnorm=I=-16:TP=-1.5:LRA=9,aformat=channel_layouts=stereo,asplit=2[voiceout][side]"
    )
    bgm_index = len(segments) + 1
    duration = float(manifest["target_duration"])
    fade_out_start = max(0.0, duration - 3.0)
    filters.append(
        f"[{bgm_index}:a]atrim=0:{duration:.3f},loudnorm=I=-28:TP=-4:LRA=7,"
        f"afade=t=in:st=0:d=1.2,afade=t=out:st={fade_out_start:.3f}:d=3[bg]"
    )
    filters.append("[bg][side]sidechaincompress=threshold=0.018:ratio=8:attack=15:release=280[duck]")
    filters.append(
        "[voiceout][duck]amix=inputs=2:duration=longest:normalize=0,"
        "loudnorm=I=-16:TP=-1.2:LRA=10,aresample=48000[aout]"
    )

    command += [
        "-filter_complex",
        ";".join(filters),
        "-map",
        "0:v:0",
        "-map",
        "[aout]",
        "-vf",
        ass_filter_path(args.subtitles),
        "-t",
        f"{duration:.3f}",
        "-c:v",
        "libx264",
        "-preset",
        "medium",
        "-crf",
        "18",
        "-pix_fmt",
        "yuv420p",
        "-r",
        "30",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        "-movflags",
        "+faststart",
        str(args.output),
    ]

    if args.dry_run:
        print(shlex.join(command))
        return
    args.output.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(command, check=True)
    print(json.dumps({"output": str(args.output.resolve()), "duration": duration}, ensure_ascii=False))


if __name__ == "__main__":
    main()
