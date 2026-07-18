"""
make_ascii_svg.py
-----------------
Converts source-prepped.png into a self-typing animated SVG.
Run locally after prep_photo.py.
Usage: python scripts/make_ascii_svg.py
Output: harsh-ascii.svg
"""

import os
import numpy as np
from PIL import Image

# ASCII density ramp: bright (sparse) -> dark (dense)
RAMP = " .`:-=+*cs#%@"

# Output grid size (cols x rows)
COLS = 90
ROWS = 48

# Visual settings - orange theme
FONT_SIZE    = 7        # px, monospace char size
CHAR_W       = FONT_SIZE * 0.6
CHAR_H       = FONT_SIZE * 1.2
FILL_COLOR   = "#c0c0c0"   # light gray for clean look
BG_COLOR     = "#0d1117"   # GitHub dark
CURSOR_COLOR = "#ff6a00"   # orange cursor

# Animation timing
ROW_DELAY    = 0.04   # seconds between each row appearing
CURSOR_SPEED = 0.6    # seconds to wipe across one row

INPUT  = "source-prepped.png"
OUTPUT = "harsh-ascii.svg"


def image_to_ascii(path: str, cols: int, rows: int) -> list[str]:
    img = Image.open(path).convert("L")
    img = img.resize((cols, rows), Image.LANCZOS)
    pixels = np.array(img)
    lines = []
    for row in pixels:
        line = ""
        for px in row:
            idx = int(px / 255 * (len(RAMP) - 1))
            line += RAMP[idx]
        lines.append(line)
    return lines


def build_svg(lines: list[str]) -> str:
    rows = len(lines)
    cols = max(len(l) for l in lines)

    svg_w = int(cols * CHAR_W) + 20
    svg_h = int(rows * CHAR_H) + 20

    parts = []
    parts.append(f'''<svg xmlns="http://www.w3.org/2000/svg"
     width="{svg_w}" height="{svg_h}"
     viewBox="0 0 {svg_w} {svg_h}">''')

    # Background
    parts.append(f'  <rect width="{svg_w}" height="{svg_h}" fill="{BG_COLOR}"/>')

    # Defs: one clip per row (horizontal wipe)
    parts.append("  <defs>")
    for i in range(rows):
        parts.append(f'    <clipPath id="r{i}">')
        parts.append(f'      <rect x="0" y="{int(i * CHAR_H) + 10}" width="0" height="{int(CHAR_H) + 2}">')
        begin = i * ROW_DELAY
        end   = begin + CURSOR_SPEED
        parts.append(f'        <animate attributeName="width" from="0" to="{svg_w}"'
                     f' begin="{begin:.2f}s" dur="{CURSOR_SPEED:.2f}s" fill="freeze"/>')
        parts.append(f'      </rect>')
        parts.append(f'    </clipPath>')
    parts.append("  </defs>")

    # Text rows
    for i, line in enumerate(lines):
        y     = int((i + 1) * CHAR_H) + 10
        begin = i * ROW_DELAY
        # Escape XML special chars
        safe = (line.replace("&", "&amp;")
                    .replace("<", "&lt;")
                    .replace(">", "&gt;")
                    .replace('"', "&quot;"))
        parts.append(
            f'  <text x="10" y="{y}" '
            f'font-family="\'Courier New\', Courier, monospace" '
            f'font-size="{FONT_SIZE}" fill="{FILL_COLOR}" '
            f'clip-path="url(#r{i})" '
            f'xml:space="preserve">{safe}</text>'
        )

    # Orange cursor block that sweeps each row then disappears
    total_dur = rows * ROW_DELAY + CURSOR_SPEED + 0.1
    parts.append(
        f'  <rect id="cursor" width="{int(CHAR_W)}" height="{int(CHAR_H)}" '
        f'fill="{CURSOR_COLOR}" opacity="0.8">'
    )
    # Move cursor row by row
    x_vals = [f"10"] + [f"{int(CHAR_W * COLS) + 10}"] * 2
    y_vals = []
    key_times = []
    for i in range(rows):
        t_start = i * ROW_DELAY
        t_end   = t_start + CURSOR_SPEED
        y_vals.append(str(int(i * CHAR_H) + 10))
        y_vals.append(str(int(i * CHAR_H) + 10))
        key_times.append(f"{t_start / total_dur:.3f}")
        key_times.append(f"{t_end / total_dur:.3f}")

    parts.append(
        f'    <animate attributeName="y" '
        f'values="{";".join(y_vals)}" '
        f'keyTimes="{";".join(key_times)}" '
        f'dur="{total_dur:.2f}s" fill="freeze"/>'
    )
    parts.append(
        f'    <animate attributeName="opacity" '
        f'values="0.8" '
        f'begin="0s" dur="{total_dur:.2f}s" fill="freeze"/>'
    )
    # Hide cursor at end
    parts.append(
        f'    <animate attributeName="opacity" '
        f'values="0.8;0" '
        f'begin="{total_dur:.2f}s" dur="0.1s" fill="freeze"/>'
    )
    parts.append('  </rect>')
    parts.append('</svg>')

    return "\n".join(parts)


def main():
    if not os.path.exists(INPUT):
        print(f"ERROR: {INPUT} not found. Run prep_photo.py first.")
        return

    print(f"Converting {INPUT} to ASCII ({COLS}×{ROWS})...")
    lines = image_to_ascii(INPUT, COLS, ROWS)

    print(f"Building animated SVG → {OUTPUT}...")
    svg = build_svg(lines)

    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write(svg)

    print(f"Done! Upload {OUTPUT} to your HarshPatil30 repo.")


if __name__ == "__main__":
    main()