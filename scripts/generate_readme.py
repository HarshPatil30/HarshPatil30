#!/usr/bin/env python3
"""Generate README.md from shared components and profile data.

Usage:
    python scripts/generate_readme.py          # writes README.md in repo root
    python scripts/generate_readme.py --check  # exits non-zero if README.md
                                                # would change (CI-friendly)
"""

from __future__ import annotations

import sys
from pathlib import Path

from profile_data import (
    BOOT_LINES,
    CONNECTION_LINES,
    DIAGNOSTICS_LINES,
    EMAIL,
    FRAMEWORKS,
    GITHUB_URL,
    HANDLE,
    LANGUAGES,
    LINKEDIN_URL,
    LOCATION,
    LOOP_LINES,
    ML_DATA,
    NAME,
    PROJECTS,
    TOOLS,
    UNIVERSITY,
)
from readme_components import (
    ACCENT,
    BG,
    GITHUB_USER,
    capsule_footer,
    capsule_header,
    divider,
    link_badge,
    project_card,
    section_header,
    status_badge,
    tech_badge,
    typing_svg,
)

REPO_ROOT = Path(__file__).resolve().parent.parent
BR = "<br/>"
BR2 = "<br/><br/>"


def _badge_row(items: list[tuple[str, str]]) -> str:
    return "\n".join(tech_badge(label, logo) for label, logo in items)


def _project_pair(left: dict, right: dict) -> str:
    """Render two project cards side-by-side in a table row."""
    lc = project_card(
        left["name"], left["stack"], left["type"], left["description"], left["url"]
    )
    rc = project_card(
        right["name"], right["stack"], right["type"], right["description"], right["url"]
    )
    return (
        "<tr>\n"
        f'<td width="50%" valign="top">\n\n{lc}\n\n</td>\n'
        f'<td width="50%" valign="top">\n\n{rc}\n\n</td>\n'
        "</tr>"
    )


def build_readme() -> str:
    parts: list[str] = []

    def add(*lines: str) -> None:
        parts.extend(lines)

    # ── Header ───────────────────────────────────────────────────────────
    add(
        "<!-- HARSH PATIL - GITHUB PROFILE -->",
        "",
        '<div align="center">',
        "",
        "<!-- ANIMATED NAME HEADER -->",
        capsule_header(),
        "",
        "<!-- GLITCH NAME ANIMATION -->",
        f'<img src="https://raw.githubusercontent.com/{GITHUB_USER}/{GITHUB_USER}/main/glitch.svg" width="100%" height="160"/>',
        "",
        BR,
        "",
        "<!-- OPENING BOOT SEQUENCE - plays once -->",
        typing_svg(
            BOOT_LINES,
            size=15,
            duration=1200,
            pause=300,
            width=700,
            height=90,
            multiline=True,
            repeat=False,
            alt="Boot Sequence",
        ),
        "",
        BR,
        "",
        "<!-- LOOPING TYPING ANIMATION -->",
        typing_svg(
            LOOP_LINES,
            size=22,
            duration=3000,
            pause=1000,
            width=600,
            link="https://git.io/typing-svg",
        ),
        "",
        BR2,
        "",
        "<!-- STATUS BADGES -->",
        link_badge("GITHUB", GITHUB_USER, "github", GITHUB_URL, alt="GitHub"),
        status_badge("STATUS", "ONLINE", alt="Status"),
        "",
        BR2,
        "",
        divider(),
        "",
        "</div>",
        "",
        BR,
    )

    # ── System Diagnostics ───────────────────────────────────────────────
    add(
        "",
        '<div align="center">',
        "",
        section_header("SYSTEM DIAGNOSTICS"),
        "",
        typing_svg(DIAGNOSTICS_LINES, duration=2000, pause=600, width=500),
        "",
        "</div>",
        "",
        BR,
        "",
    )

    # Identity + config table
    add(
        '<table width="100%" border="0" cellspacing="20" cellpadding="0">',
        "<tr>",
        '<td width="50%" valign="top">',
        "",
        "```",
        "╔════════════════════════════════════════╗",
        "║        > PROCESS: HARSH.EXE           ║",
        "╠════════════════════════════════════════╣",
        "║                                        ║",
        "║  [IDENTITY]                            ║",
        f"║   NAME   ::  {NAME:<25}║",
        f"║   HANDLE ::  {HANDLE:<25}║",
        f"║   NODE   ::  {'Hubballi, KA, IN':<25}║",
        f"║   INST   ::  {'KLE Tech University':<25}║",
        "║                                        ║",
        "╠════════════════════════════════════════╣",
        "║                                        ║",
        "║  [RUNTIME STATUS]                      ║",
        "║   MODE   ::  Builder                  ║",
        "║   BUILD  ::  Context-Aware ML         ║",
        "║   UPTIME ::  99.9%                    ║",
        '║   LOG    ::  "Ideas are everything"   ║',
        "║                                        ║",
        "╚════════════════════════════════════════╝",
        "```",
        "",
        "</td>",
        '<td width="50%" valign="top">',
        "",
        "```javascript",
        "// harsh.config.js",
        "",
        "module.exports = {",
        f'  name     : "{NAME}",',
        f'  handle   : "{HANDLE}",',
        f'  location : "{LOCATION}",',
        f'  education: "{UNIVERSITY}",',
        "",
        "  languages: [",
        '    "Python", "JavaScript",',
        '    "C++", "Java", "TypeScript"',
        "  ],",
        "",
        "  interests: [",
        '    "Machine Learning",',
        '    "NLP & Deep Learning",',
        '    "Full Stack Development",',
        '    "EdTech & Open Source"',
        "  ],",
        "",
        '  currently: "Context-Aware ML Systems",',
        "",
        "  debug: () => {",
        '    console.log("it works!");',
        "    // ^ and I'm proud of it",
        "  }",
        "};",
        "```",
        "",
        "</td>",
        "</tr>",
        "</table>",
        "",
        BR,
    )

    # ── Featured Projects ────────────────────────────────────────────────
    add(
        "",
        '<div align="center">',
        divider(),
        "",
        BR2,
        "",
        section_header("FEATURED PROJECTS"),
        "",
        typing_svg(
            ["Scanning project database...", "4 records found."],
            duration=2000,
            pause=500,
            width=435,
        ),
        "",
        "</div>",
        "",
        BR,
        "",
        '<table width="100%" border="0" cellspacing="20" cellpadding="0">',
    )
    for i in range(0, len(PROJECTS), 2):
        add(_project_pair(PROJECTS[i], PROJECTS[i + 1]))
    add("</table>", "", BR)

    # ── Tech Arsenal ─────────────────────────────────────────────────────
    add(
        "",
        '<div align="center">',
        divider(),
        "",
        BR2,
        "",
        section_header("TECH ARSENAL"),
        "",
        typing_svg(["Loading tech stack..."], duration=1500, width=300),
        "",
        BR2,
        "",
        "**LANGUAGES**",
        "",
        _badge_row(LANGUAGES),
        "",
        BR,
        "",
        "**ML / DATA**",
        "",
        _badge_row(ML_DATA),
        "",
        BR,
        "",
        "**FRAMEWORKS**",
        "",
        _badge_row(FRAMEWORKS),
        "",
        BR,
        "",
        "**TOOLS & PLATFORMS**",
        "",
        _badge_row(TOOLS),
        "",
        BR2,
        "",
        divider(),
        "",
        BR2,
    )

    # ── System Metrics ───────────────────────────────────────────────────
    add(
        "",
        section_header("SYSTEM METRICS"),
        "",
        typing_svg(["Fetching GitHub analytics..."], duration=1500, width=350),
        "",
        BR2,
        "",
        f'<img src="https://github-readme-activity-graph.vercel.app/graph'
        f"?username={GITHUB_USER}&bg_color={BG}&color=ff9a3c&line={ACCENT}"
        f"&point={ACCENT}&area=true&area_color={ACCENT}"
        '&hide_border=true" width="100%"/>',
        "",
        BR2,
        "",
        divider(),
        "",
        BR2,
    )

    # ── Contribution Snake ───────────────────────────────────────────────
    add(
        "",
        section_header("CONTRIBUTION SNAKE"),
        "",
        typing_svg(["Rendering contribution snake..."], duration=1500, width=350),
        "",
        BR2,
        "",
        f"![Snake animation](https://raw.githubusercontent.com/{GITHUB_USER}/{GITHUB_USER}/output/github-contribution-grid-snake-dark.svg)",
        "",
        BR2,
        "",
        divider(),
        "",
        BR2,
    )

    # ── Establish Connection ─────────────────────────────────────────────
    add(
        "",
        section_header("ESTABLISH CONNECTION"),
        "",
        typing_svg(CONNECTION_LINES, size=18, duration=2000, pause=1000, width=500),
        "",
        BR2,
        "",
        link_badge("LINKEDIN", "CONNECT", "linkedin", LINKEDIN_URL, alt="LinkedIn"),
        link_badge("GITHUB", "FOLLOW", "github", GITHUB_URL, alt="GitHub"),
        link_badge("EMAIL", "PING_ME", "gmail", f"mailto:{EMAIL}", alt="Email"),
        "",
        BR2,
        "",
        "```",
        "> session.end()",
        "  — thanks for visiting. now go build something. —",
        "```",
        "",
        BR,
        "",
        "<!-- FOOTER WAVE -->",
        capsule_footer(),
        "",
        "</div>",
    )

    return "\n".join(parts) + "\n"


def main() -> None:
    check_mode = "--check" in sys.argv
    expected = build_readme()
    readme_path = REPO_ROOT / "README.md"

    if check_mode:
        current = readme_path.read_text() if readme_path.exists() else ""
        if current != expected:
            print("README.md is out of date. Run: python scripts/generate_readme.py")
            sys.exit(1)
        print("README.md is up to date.")
        sys.exit(0)

    readme_path.write_text(expected)
    print(f"Wrote {readme_path}")


if __name__ == "__main__":
    main()
