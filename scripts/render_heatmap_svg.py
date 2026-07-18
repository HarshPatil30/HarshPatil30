"""
render_heatmap_svg.py
---------------------
Reads data/contributions.json and renders an animated contribution
heatmap SVG in Harsh's orange theme.
Run after fetch_contributions.py.
Usage: python scripts/render_heatmap_svg.py
Output: contrib-heatmap.svg
"""

import json
import math
from datetime import datetime

INPUT  = "data/contributions.json"
OUTPUT = "contrib-heatmap.svg"

# Orange theme palette (none → brightest)
PALETTE = [
    "#161b22",  # level 0 — empty
    "#3d1a00",  # level 1
    "#7a3500",  # level 2
    "#b85000",  # level 3
    "#ff6a00",  # level 4
    "#ff9a3c",  # level 5 — max
]

BG_COLOR     = "#0d1117"
LABEL_COLOR  = "#8b949e"
TITLE_COLOR  = "#ff6a00"
STATS_COLOR  = "#ff9a3c"
FONT         = "'Courier New', Courier, monospace"

BOX_SIZE  = 11   # px per day square
BOX_GAP   = 3    # gap between squares
WEEK_W    = BOX_SIZE + BOX_GAP
DAY_H     = BOX_SIZE + BOX_GAP

PAD_LEFT  = 30   # space for day labels
PAD_TOP   = 50   # space for month labels + title
PAD_BOT   = 50   # space for stats footer
PAD_RIGHT = 20

WEEKS     = 53
DAYS      = 7

SVG_W = PAD_LEFT + WEEKS * WEEK_W + PAD_RIGHT
SVG_H = PAD_TOP  + DAYS  * DAY_H  + PAD_BOT

# Animation
DIAG_DELAY = 0.015   # seconds per diagonal step
REVEAL_DUR  = 0.18   # fade-in duration per box


def level_color(level: int) -> str:
    return PALETTE[min(level, len(PALETTE) - 1)]


def build_svg(data: dict) -> str:
    days_list = data["days"]
    stats     = data["stats"]

    # Index by date
    by_date = {d["date"]: d for d in days_list}

    # Build 53×7 grid (week col, day row) from the data
    # Pad to exactly 53 weeks starting from the earliest Sunday
    if not days_list:
        return "<svg/>"

    first = datetime.strptime(days_list[0]["date"], "%Y-%m-%d")
    # Walk back to Sunday
    offset = first.weekday() + 1  # Monday=0 so Sunday offset
    if offset == 7:
        offset = 0

    parts = []
    parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{SVG_W}" height="{SVG_H}" '
        f'viewBox="0 0 {SVG_W} {SVG_H}">'
    )
    parts.append(f'  <rect width="{SVG_W}" height="{SVG_H}" fill="{BG_COLOR}" rx="8"/>')

    # Title
    parts.append(
        f'  <text x="{SVG_W // 2}" y="22" text-anchor="middle" '
        f'font-family="{FONT}" font-size="13" font-weight="bold" '
        f'fill="{TITLE_COLOR}">Harsh Patil\'s Contribution Graph</text>'
    )

    # Month labels
    MONTHS = ["Jan","Feb","Mar","Apr","May","Jun",
              "Jul","Aug","Sep","Oct","Nov","Dec"]
    last_month = -1
    for w in range(WEEKS):
        # Estimate date for this column
        day_idx = w * 7
        if day_idx < len(days_list):
            d = datetime.strptime(days_list[day_idx]["date"], "%Y-%m-%d")
            if d.month != last_month:
                x = PAD_LEFT + w * WEEK_W
                parts.append(
                    f'  <text x="{x}" y="{PAD_TOP - 6}" '
                    f'font-family="{FONT}" font-size="9" fill="{LABEL_COLOR}">'
                    f'{MONTHS[d.month - 1]}</text>'
                )
                last_month = d.month

    # Day labels (Mon, Wed, Fri)
    DAY_LABELS = {1: "Mon", 3: "Wed", 5: "Fri"}
    for row, label in DAY_LABELS.items():
        y = PAD_TOP + row * DAY_H + BOX_SIZE - 1
        parts.append(
            f'  <text x="{PAD_LEFT - 4}" y="{y}" text-anchor="end" '
            f'font-family="{FONT}" font-size="9" fill="{LABEL_COLOR}">'
            f'{label}</text>'
        )

    # Day squares with diagonal reveal animation
    day_ptr = 0
    for w in range(WEEKS):
        for d in range(DAYS):
            if day_ptr < len(days_list):
                day_data = days_list[day_ptr]
                day_ptr += 1
            else:
                day_data = {"level": 0, "count": 0, "date": ""}

            x = PAD_LEFT + w * WEEK_W
            y = PAD_TOP  + d * DAY_H
            color = level_color(day_data["level"])

            # Diagonal index for staggered animation
            diag  = w + d
            begin = diag * DIAG_DELAY

            title = ""
            if day_data.get("date"):
                cnt   = day_data["count"]
                label = f"{cnt} contribution{'s' if cnt != 1 else ''} on {day_data['date']}"
                title = f"<title>{label}</title>"

            parts.append(
                f'  <rect x="{x}" y="{y}" width="{BOX_SIZE}" height="{BOX_SIZE}" '
                f'rx="2" fill="{color}" opacity="0">'
                f'{title}'
                f'<animate attributeName="opacity" from="0" to="1" '
                f'begin="{begin:.3f}s" dur="{REVEAL_DUR:.2f}s" fill="freeze"/>'
                f'</rect>'
            )

    # Legend
    legend_x = SVG_W - PAD_RIGHT - 6 * (BOX_SIZE + 4) - 30
    legend_y  = SVG_H - PAD_BOT + 20
    parts.append(
        f'  <text x="{legend_x - 4}" y="{legend_y + BOX_SIZE}" '
        f'font-family="{FONT}" font-size="9" fill="{LABEL_COLOR}" '
        f'text-anchor="end">Less</text>'
    )
    for li, col in enumerate(PALETTE):
        lx = legend_x + li * (BOX_SIZE + 4)
        parts.append(
            f'  <rect x="{lx}" y="{legend_y}" '
            f'width="{BOX_SIZE}" height="{BOX_SIZE}" rx="2" fill="{col}"/>'
        )
    parts.append(
        f'  <text x="{legend_x + len(PALETTE) * (BOX_SIZE + 4) + 4}" '
        f'y="{legend_y + BOX_SIZE}" '
        f'font-family="{FONT}" font-size="9" fill="{LABEL_COLOR}">More</text>'
    )

    # Stats footer
    total   = stats.get("total", 0)
    streak  = stats.get("current_streak", 0)
    longest = stats.get("longest_streak", 0)
    footer  = (f"{total} contributions in the last year  ·  "
               f"Current streak: {streak}  ·  "
               f"Longest streak: {longest}")
    parts.append(
        f'  <text x="{SVG_W // 2}" y="{SVG_H - 10}" text-anchor="middle" '
        f'font-family="{FONT}" font-size="10" fill="{STATS_COLOR}">'
        f'{footer}</text>'
    )

    parts.append('</svg>')
    return "\n".join(parts)


def main():
    try:
        with open(INPUT, encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"ERROR: {INPUT} not found. Run fetch_contributions.py first.")
        return

    print(f"Rendering heatmap → {OUTPUT}...")
    svg = build_svg(data)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Done! {OUTPUT} is ready to commit.")


if __name__ == "__main__":
    main()