"""Shared utility functions for generating README.md components.

Eliminates duplication by centralizing badge generation, typing SVG animations,
dividers, project cards, and section headers into reusable helpers. All theme
constants (colors, fonts, URLs) are defined once here.
"""

from urllib.parse import quote as _url_quote


def _encode_line(text: str) -> str:
    """URL-encode a typing-SVG line, preserving apostrophes unencoded."""
    return _url_quote(text, safe="'")


# ── Theme constants ──────────────────────────────────────────────────────────
ACCENT = "ff6a00"
ACCENT_UPPER = "FF6A00"
BG = "0d1117"
FONT = "Share+Tech+Mono"
DIVIDER_URL = (
    "https://user-images.githubusercontent.com/73097560/"
    "115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif"
)
TYPING_SVG_BASE = "https://readme-typing-svg.demolab.com"
BADGE_BASE = "https://img.shields.io/badge"
GITHUB_USER = "HarshPatil30"


# ── Divider ──────────────────────────────────────────────────────────────────
def divider() -> str:
    """Full-width animated divider (was copy-pasted 6 times)."""
    return f'<img src="{DIVIDER_URL}" width="100%">'


# ── Typing SVG ───────────────────────────────────────────────────────────────
def typing_svg(
    lines: list[str],
    *,
    size: int = 14,
    duration: int = 2000,
    pause: int = 800,
    width: int = 350,
    height: int | None = None,
    multiline: bool = False,
    repeat: bool = True,
    alt: str = "Typing SVG",
    link: str | None = None,
) -> str:
    """Generate a readme-typing-svg ``<img>`` tag.

    All 8 typing SVGs in the original README shared font, color, and
    center/vCenter params. This helper makes those the default.
    """
    encoded_lines = ";".join(_encode_line(line).replace("%20", "+") for line in lines)
    params = (
        f"font={FONT}&size={size}&duration={duration}&pause={pause}"
        f"&color={ACCENT_UPPER}&center=true&vCenter=true"
    )
    if multiline:
        params += "&multiline=true"
    if not repeat:
        params += "&repeat=false"
    params += f"&width={width}"
    if height is not None:
        params += f"&height={height}"
    params += f"&lines={encoded_lines}"

    img = f'<img src="{TYPING_SVG_BASE}?{params}" alt="{alt}" />'

    if link:
        return f'<a href="{link}">{img}</a>'
    return img


# ── Badges ───────────────────────────────────────────────────────────────────
def tech_badge(label: str, logo: str) -> str:
    """Tech stack badge (21 of these shared the same pattern)."""
    return (
        f"![{label}]({BADGE_BASE}/{label.replace(' ', '_')}-{BG}"
        f"?style=for-the-badge&logo={logo}&logoColor={ACCENT})"
    )


def status_badge(label: str, message: str, *, alt: str | None = None) -> str:
    """Header-area status badge."""
    return (
        f"![{alt or label}]({BADGE_BASE}/{label}-{message}-{ACCENT}"
        f"?style=for-the-badge&labelColor={BG})"
    )


def link_badge(
    label: str, message: str, logo: str, url: str, *, alt: str | None = None
) -> str:
    """Clickable social / link badge."""
    return (
        f"[![{alt or label}]({BADGE_BASE}/{label}-{message}-{ACCENT}"
        f"?style=for-the-badge&logo={logo}&logoColor={ACCENT}"
        f"&labelColor={BG})]({url})"
    )


# ── Project card ─────────────────────────────────────────────────────────────
def project_card(
    name: str, stack: str, card_type: str, description: list[str], url: str
) -> str:
    """ASCII-art project card (was duplicated 4 times with identical borders).

    ``description`` is a list of lines (max ~37 chars each to fit the box).
    """
    w = 40  # inner width between the outer ║ chars
    border = "═" * w

    def row(text: str = "") -> str:
        return f"║  {text:<{w - 2}}║"

    lines = [
        f"╔{border}╗",
        row(f"PROJECT  ::  {name}"),
        f"╠{border}╣",
        row(),
        row(f"STACK    ::  {stack}"),
        row(f"TYPE     ::  {card_type}"),
        row(),
        *[row(d) for d in description],
        row(),
        f"╚{border}╝",
    ]
    card = "\n".join(lines)
    return f"```\n{card}\n```\n[→ View Repository]({url})"


# ── Section header ───────────────────────────────────────────────────────────
def section_header(title: str) -> str:
    """Section heading with bracket styling (repeated pattern)."""
    return f"## `[ {title} ]`"


# ── Capsule render ───────────────────────────────────────────────────────────
def capsule_header() -> str:
    return (
        '<img src="https://capsule-render.vercel.app/api'
        f"?type=rect&color=0:{BG},100:{BG}&height=10&section=header"
        '" width="100%"/>'
    )


def capsule_footer(text: str = "KEEP BUILDING") -> str:
    return (
        '<img src="https://capsule-render.vercel.app/api'
        f"?type=waving&color=0:{BG},100:{ACCENT}&height=120&section=footer"
        f"&text={_encode_line(text).replace('%20', '+')}&fontSize=24&fontColor={ACCENT}"
        '&animation=twinkling&fontAlignY=70" width="100%"/>'
    )
