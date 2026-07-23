import argparse
import re
import sys
from os import remove
from pathlib import Path

from PIL import Image

IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff")
VIDEO_EXTENSIONS = (".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm")


def is_image(file_path: str) -> bool:
    return any(file_path.lower().endswith(ext) for ext in IMAGE_EXTENSIONS)


def is_video(file_path: str) -> bool:
    return any(file_path.lower().endswith(ext) for ext in VIDEO_EXTENSIONS)


def parse_resolution(resolution: str) -> tuple[int, int]:
    match = re.fullmatch(r"(\d+)\s*x\s*(\d+)", resolution.strip())
    if not match:
        print(
            f"Error: Invalid resolution format '{resolution}'. Expected WxH (e.g. 1920x1080)",
            file=sys.stderr,
        )
        sys.exit(1)
    return int(match.group(1)), int(match.group(2))


def get_video_resolution(file_path: Path) -> tuple[int, int] | None:
    import cv2

    cap = cv2.VideoCapture(str(file_path))
    if not cap.isOpened():
        return None
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cap.release()
    return width, height


def delete_low_res_images(directory: Path, min_width: int, min_height: int) -> int:
    deleted = 0
    for file in directory.iterdir():
        if file.is_file() and is_image(file.name):
            with Image.open(file) as img:
                width, height = img.size
                if width < min_width or height < min_height:
                    print(f"Deleting {file.name} ({width}x{height})")
                    remove(file)
                    deleted += 1
    return deleted


def delete_low_res_videos(directory: Path, min_width: int, min_height: int) -> int:
    deleted = 0
    for file in directory.iterdir():
        if file.is_file() and is_video(file.name):
            res = get_video_resolution(file)
            if res is None:
                print(f"Skipping {file.name} (unable to read)")
                continue
            width, height = res
            if width < min_width or height < min_height:
                print(f"Deleting {file.name} ({width}x{height})")
                remove(file)
                deleted += 1
    return deleted


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Delete images or videos below a minimum resolution."
    )
    parser.add_argument(
        "directory",
        nargs="?",
        default=".",
        help="Directory to scan (default: current directory)",
    )
    parser.add_argument(
        "resolution",
        help="Minimum resolution as WxH (e.g. 1920x1080)",
    )
    parser.add_argument(
        "-v",
        "--video",
        action="store_true",
        help="Include video files",
    )
    parser.add_argument(
        "-i",
        "--image",
        action="store_true",
        help="Include image files",
    )

    args = parser.parse_args()

    if not args.video and not args.image:
        parser.error("At least one of -v or -i must be specified.")

    target = Path(args.directory)
    if not target.is_dir():
        print(f"Error: '{target}' is not a directory", file=sys.stderr)
        sys.exit(1)

    min_width, min_height = parse_resolution(args.resolution)
    deleted = 0

    if args.image:
        deleted += delete_low_res_images(target, min_width, min_height)
    if args.video:
        deleted += delete_low_res_videos(target, min_width, min_height)

    label = []
    if args.image:
        label.append("image(s)")
    if args.video:
        label.append("video(s)")
    print(f"Done. Deleted {deleted} {'/'.join(label)}.")


if __name__ == "__main__":
    main()
