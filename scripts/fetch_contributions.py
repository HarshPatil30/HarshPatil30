"""
fetch_contributions.py
----------------------
Scrapes your public GitHub contribution calendar — no token needed.
Saves data/contributions.json with raw day data + derived stats.
Run by GitHub Actions daily, or locally anytime.
Usage: python scripts/fetch_contributions.py
"""

import json
import os
from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup

USERNAME = "HarshPatil30"
URL      = f"https://github.com/users/{USERNAME}/contributions"
OUT      = "data/contributions.json"


def fetch() -> list[dict]:
    print(f"Fetching contributions from {URL}...")
    headers = {"User-Agent": "Mozilla/5.0 (profile-art-bot)"}
    r = requests.get(URL, headers=headers, timeout=15)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")
    days = []

    for td in soup.select("td.ContributionCalendar-day"):
        date_str = td.get("data-date", "")
        if not date_str:
            continue
        # count may be in tooltip or data attribute
        count_str = td.get("data-level", "0")
        # Try to get actual count from tooltip text
        label = td.get("aria-label", "")
        count = 0
        if "No contributions" in label:
            count = 0
        else:
            try:
                count = int(label.split(" contribution")[0].split()[-1])
            except (ValueError, IndexError):
                count = int(count_str)

        days.append({
            "date":  date_str,
            "count": count,
            "level": int(td.get("data-level", 0))
        })

    return days


def derive_stats(days: list[dict]) -> dict:
    total = sum(d["count"] for d in days)

    # Current streak
    today = datetime.today().date()
    streak = 0
    for i in range(len(days) - 1, -1, -1):
        d = days[i]
        day_date = datetime.strptime(d["date"], "%Y-%m-%d").date()
        if day_date > today:
            continue
        if d["count"] > 0:
            streak += 1
        else:
            break

    # Longest streak
    longest = cur = 0
    for d in days:
        if d["count"] > 0:
            cur += 1
            longest = max(longest, cur)
        else:
            cur = 0

    # Best day
    best = max(days, key=lambda d: d["count"], default={"date": "", "count": 0})

    # Monthly totals (last 12 months)
    monthly: dict[str, int] = {}
    for d in days:
        month = d["date"][:7]
        monthly[month] = monthly.get(month, 0) + d["count"]

    return {
        "total":          total,
        "current_streak": streak,
        "longest_streak": longest,
        "best_day":       best,
        "monthly":        monthly,
        "fetched_at":     datetime.utcnow().isoformat() + "Z",
    }


def main():
    os.makedirs("data", exist_ok=True)
    days  = fetch()
    stats = derive_stats(days)
    payload = {"days": days, "stats": stats}

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    print(f"Saved {len(days)} days → {OUT}")
    print(f"  Total: {stats['total']}  |  "
          f"Streak: {stats['current_streak']}  |  "
          f"Longest: {stats['longest_streak']}")
    print("Now run: python scripts/render_heatmap_svg.py")


if __name__ == "__main__":
    main()