from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable

import cv2


VIDEO_EXTS = {".mp4", ".avi", ".mov", ".mkv", ".m4v"}


def iter_video_files(input_path: Path) -> Iterable[Path]:
    if input_path.is_file():
        yield input_path
        return

    if input_path.is_dir():
        for p in sorted(input_path.iterdir()):
            if p.is_file() and p.suffix.lower() in VIDEO_EXTS:
                yield p
        return

    raise FileNotFoundError(f"Input not found: {input_path}")


def extract_every_nth_frame(video_path: Path, output_dir: Path, step: int) -> tuple[int, int]:
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        raise RuntimeError(f"Unable to open video: {video_path}")

    video_stem = video_path.stem
    total = 0
    saved = 0

    while True:
        ok, frame = cap.read()
        if not ok:
            break

        if total % step == 0:
            out_path = output_dir / f"{video_stem}_frame_{total:06d}.jpg"
            if not cv2.imwrite(str(out_path), frame):
                raise RuntimeError(f"Failed to write image: {out_path}")
            saved += 1

        total += 1

    cap.release()
    return total, saved


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract 1 frame every N frames from a video (or all videos in a folder)."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("videos/potatos.mp4"),
        help="Video file path OR folder containing videos (default: videos/potatos.mp4)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("dataset/frames"),
        help="Output folder for extracted frames (default: dataset/frames)",
    )
    parser.add_argument(
        "--step",
        type=int,
        default=6,
        help="Take 1 frame every N frames (default: 6)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.step <= 0:
        raise SystemExit("--step must be >= 1")

    input_path = args.input
    output_dir = args.output

    output_dir.mkdir(parents=True, exist_ok=True)

    videos = list(iter_video_files(input_path))
    if not videos:
        raise SystemExit(f"No video files found in: {input_path}")

    grand_total = 0
    grand_saved = 0

    for vp in videos:
        total, saved = extract_every_nth_frame(vp, output_dir, args.step)
        grand_total += total
        grand_saved += saved
        print(f"{vp.name}: read={total}, saved={saved} -> {output_dir}")

    print(f"DONE: read={grand_total}, saved={grand_saved} (step={args.step})")


if __name__ == "__main__":
    main()
