"""
prep_photo.py
-------------
Run once whenever you change your profile photo.
Usage: python scripts/prep_photo.py <path-to-photo.jpg>
Output: source-prepped.png (grayscale, background removed, contrast boosted)
"""

import sys
import numpy as np
import cv2
from PIL import Image
from rembg import remove

def prep(input_path: str, output_path: str = "source-prepped.png"):
    print(f"[1/3] Removing background from {input_path}...")
    with open(input_path, "rb") as f:
        raw = f.read()
    no_bg = remove(raw)

    img = Image.open(__import__("io").BytesIO(no_bg)).convert("RGBA")

    # Composite onto white background
    white = Image.new("RGBA", img.size, (255, 255, 255, 255))
    white.paste(img, mask=img.split()[3])
    gray = white.convert("L")

    print("[2/3] Boosting local contrast with CLAHE...")
    gray_np = np.array(gray)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray_np)

    print("[3/3] Saving to", output_path)
    Image.fromarray(enhanced).save(output_path)
    print("Done. Now run: python scripts/make_ascii_svg.py")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/prep_photo.py <photo.jpg>")
        sys.exit(1)
    prep(sys.argv[1])