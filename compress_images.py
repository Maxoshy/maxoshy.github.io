
from pathlib import Path
from PIL import Image, ImageOps
import os

SOURCE = Path("images")
OUTPUT = Path("images-compressed")
MAX_SIZE = 2000
JPEG_QUALITY = 82

OUTPUT.mkdir(exist_ok=True)

total_before = 0
total_after = 0

for path in SOURCE.iterdir():
    if not path.is_file():
        continue

    if path.suffix.lower() not in {".jpg", ".jpeg", ".png"}:
        continue

    try:
        with Image.open(path) as original:
            before = path.stat().st_size
            image = ImageOps.exif_transpose(original)
            image.thumbnail((MAX_SIZE, MAX_SIZE))

            destination = OUTPUT / path.name

            if path.suffix.lower() in {".jpg", ".jpeg"}:
                if image.mode not in ("RGB", "L"):
                    image = image.convert("RGB")

                image.save(
                    destination,
                    "JPEG",
                    quality=JPEG_QUALITY,
                    optimize=True,
                    progressive=True
                )

            else:
                image.save(
                    destination,
                    "PNG",
                    optimize=True
                )

            after = destination.stat().st_size
            total_before += before
            total_after += after

            saved = (1 - after / before) * 100
            print(f"{path.name}: {before / 1024:.0f} KB"
                  f" -> {after / 1024:.0f} KB ({saved:.0f}% smaller)")

    except Exception as error:
        print(f"Skipped {path.name}: {error}")

print("\n--- TOTALS ---")
print(f"Original:   {total_before / 1024 / 1024:.2f} MB")
print(f"Compressed: {total_after / 1024 / 1024:.2f} MB")

if total_before:
    print(f"Space saved: {(1 - total_after / total_before) * 100:.1f}%")

print(f"\nCompressed copies saved in: {OUTPUT}")

