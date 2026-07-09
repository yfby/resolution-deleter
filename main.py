from os import remove
from pathlib import Path

from PIL import Image

directory_path = Path(".")


def is_image(file_path: str) -> bool:
    image_extensions = [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff"]
    return any(file_path.lower().endswith(ext) for ext in image_extensions)


for file in directory_path.iterdir():
    if file.is_file():
        if is_image(file.name):
            with Image.open(file) as img:
                width, height = img.size
                if width < 1920 or height < 1080:
                    print(f"Deleting {file.name} (size: {width}x{height})")
                    remove(file)
