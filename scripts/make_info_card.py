"""
make_info_card.py
-----------------
Generates a neofetch-style animated info card SVG.
Run locally whenever you update your info.
Usage: python scripts/make_info_card.py
Output: info-card.svg
"""

import os

OUTPUT = "info-card.svg"

# ── YOUR INFO ─────────────────────────────────────────────────
USER = "HarshPatil30"
INFO = [
    ("OS",       "Builder Mode · Hubballi, IN"),
    ("Host",     "KLE Technological University"),
    ("Role",     "CS Engineer · 3rd Year"),
    ("Shell",    "Python · JavaScript · C++"),
    ("Stack",    "ML · NLP · React · Node.js"),
    ("Focus",    "Context-Aware ML Systems"),
    ("Open",     "Collabs · Internships · Ideas"),
    ("Uptime",   "99.9%  |  Status: ONLINE"),
    ("Contact",  "patilharsh3006@gmail.com"),
    ("GitHub",   "github.com/HarshPatil30"),
]
# ──────────────────────────────────────────────────────────────

BG_COLOR     = "#0d1117"
BORDER_COLOR = "#ff6a00"
KEY_COLOR    = "#ff6a00"
VAL_COLOR    = "#e0e0e0"
TITLE_COLOR  = "#ffffff"
DIM_COLOR    = "#555555"

FONT         = "'Courier New', Courier, monospace"
FONT_SIZE    = 13
LINE_H       = 22
PAD_X        = 18
PAD_Y        = 18

STATIC       = os.environ.get("STATIC", "0") == "1"

# Dimensions
W = 480
HEADER_H = 52
ROWS_H   = len(INFO) * LINE_H + 16
H        = HEADER_H + ROWS_H + PAD_Y

TOTAL_DUR  = 0.0
LINE_DELAY = 0.12   # seconds between each line fading in
FADE_DUR   = 0.25


def anim(i: int, attr: str, from_v, to_v, extra="") -> str:
    if STATIC:
        return ""
    begin = i * LINE_DELAY
    return (f'<animate attributeName="{attr}" '
            f'from="{from_v}" to="{to_v}" '
            f'begin="{begin:.2f}s" dur="{FADE_DUR:.2f}s" '
            f'fill="freeze" {extra}/>' )


def build_svg() -> str:
    parts = []
    parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
    )

    # Background
    parts.append(f'  <rect width="{W}" height="{H}" fill="{BG_COLOR}" rx="6"/>')

    # Border
    parts.append(
        f'  <rect x="1" y="1" width="{W-2}" height="{H-2}" '
        f'fill="none" stroke="{BORDER_COLOR}" stroke-width="1.5" rx="6"/>'
    )

    # Title bar
    parts.append(
        f'  <rect x="0" y="0" width="{W}" height="{HEADER_H}" '
        f'fill="{BORDER_COLOR}" rx="6"/>'
    )
    parts.append(
        f'  <rect x="0" y="{HEADER_H - 6}" width="{W}" height="6" fill="{BORDER_COLOR}"/>'
    )

    # Terminal dots
    for idx, color in enumerate(["#ff5f57", "#febc2e", "#28c840"]):
        cx = PAD_X + idx * 20
        parts.append(f'  <circle cx="{cx}" cy="22" r="6" fill="{color}"/>')

    # Title text
    title = f"{USER}@github ~ $ neofetch"
    parts.append(
        f'  <text x="{W // 2}" y="30" text-anchor="middle" '
        f'font-family="{FONT}" font-size="13" font-weight="bold" '
        f'fill="{TITLE_COLOR}">{title}</text>'
    )

    # Color blocks (like neofetch palette)
    block_y = HEADER_H + 8
    colors  = [BORDER_COLOR, "#ff9a3c", "#ffd700", "#39d353",
               "#00bfff", "#bf5fff", "#ff69b4", "#ffffff"]
    bw = (W - PAD_X * 2) // len(colors)
    for ci, col in enumerate(colors):
        parts.append(
            f'  <rect x="{PAD_X + ci * bw}" y="{block_y}" '
            f'width="{bw - 2}" height="8" fill="{col}" rx="2"/>'
        )

    # Info lines
    y_start = HEADER_H + 30
    for i, (key, val) in enumerate(INFO):
        y = y_start + i * LINE_H
        opacity_start = "0" if not STATIC else "1"

        # Key
        parts.append(
            f'  <text x="{PAD_X}" y="{y}" '
            f'font-family="{FONT}" font-size="{FONT_SIZE}" '
            f'fill="{KEY_COLOR}" opacity="{opacity_start}">'
            f'{anim(i, "opacity", 0, 1)}'
            f'{key}</text>'
        )

        # Separator
        sep_x = PAD_X + 90
        parts.append(
            f'  <text x="{sep_x}" y="{y}" '
            f'font-family="{FONT}" font-size="{FONT_SIZE}" '
            f'fill="{DIM_COLOR}" opacity="{opacity_start}">'
            f'{anim(i, "opacity", 0, 1)}'
            f'··</text>'
        )

        # Value
        val_x = sep_x + 20
        parts.append(
            f'  <text x="{val_x}" y="{y}" '
            f'font-family="{FONT}" font-size="{FONT_SIZE}" '
            f'fill="{VAL_COLOR}" opacity="{opacity_start}">'
            f'{anim(i, "opacity", 0, 1)}'
            f'{val}</text>'
        )

    parts.append('</svg>')
    return "\n".join(parts)


def main():
    print(f"Building info card → {OUTPUT}...")
    svg = build_svg()
    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Done! Upload {OUTPUT} to your HarshPatil30 repo.")


if __name__ == "__main__":
    main()