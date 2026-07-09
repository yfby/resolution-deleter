import argparse
import sys
from os import remove
from pathlib import Path

from PIL import Image

IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff")


def is_image(file_path: str) -> bool:
    return any(file_path.lower().endswith(ext) for ext in IMAGE_EXTENSIONS)


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


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Delete images below a minimum resolution."
    )
    parser.add_argument(
        "directory",
        nargs="?",
        default=".",
        help="Directory to scan (default: current directory)",
    )
    parser.add_argument(
        "--min-width",
        type=int,
        default=1920,
        help="Minimum width in pixels (default: 1920)",
    )
    parser.add_argument(
        "--min-height",
        type=int,
        default=1080,
        help="Minimum height in pixels (default: 1080)",
    )

    args = parser.parse_args()
    target = Path(args.directory)

    if not target.is_dir():
        print(f"Error: '{target}' is not a directory", file=sys.stderr)
        sys.exit(1)

    deleted = delete_low_res_images(target, args.min_width, args.min_height)
    print(f"Done. Deleted {deleted} image(s).")


if __name__ == "__main__":
    main()
