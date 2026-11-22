#!/usr/bin/env python3
"""Build the 22 November 2026 front page as one 1024x1024 PNG.

The page is a newspaper front: a navy masthead with the date, a hero
illustration, four main stories in a two-by-two grid, an IN BRIEF band
with four short items, and a footer. Headlines were checked against news
reports dated 22 November 2026. Run from the repo root:

    python3 draw_frontpage.py

and entry.png appears next to this script.
"""
import os

from PIL import Image as PilImage
from PIL import ImageDraw as PilDraw
from PIL import ImageFont as PilFont

PAGE_W = 1024
PAGE_H = 1024
MARGIN = 36
GUTTER = 512
COL_W = 452
MASTHEAD_H = 108
HERO_H = 260

PAPER = (246, 241, 231)
NAVY_INK = (27, 47, 74)
GOLD_LINE = (201, 162, 39)
ALERT_RED = (176, 30, 30)
BODY_INK = (26, 26, 26)
MUTED = (85, 85, 85)
HAIRLINE = (170, 165, 155)
WHITE = (255, 255, 255)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def load_fonts():
    """Return the four typefaces the page uses, keyed by role."""
    return {
        "masthead": PilFont.truetype(f"{FONT_DIR}/DejaVuSerif-Bold.ttf", 62),
        "date": PilFont.truetype(f"{FONT_DIR}/DejaVuSans-Bold.ttf", 19),
        "kicker": PilFont.truetype(f"{FONT_DIR}/DejaVuSans-Bold.ttf", 17),
        "headline": PilFont.truetype(f"{FONT_DIR}/DejaVuSerif-Bold.ttf", 30),
        "deck": PilFont.truetype(f"{FONT_DIR}/DejaVuSans.ttf", 17),
        "section": PilFont.truetype(f"{FONT_DIR}/DejaVuSans-Bold.ttf", 19),
        "brief_head": PilFont.truetype(f"{FONT_DIR}/DejaVuSans-Bold.ttf", 16),
        "brief_deck": PilFont.truetype(f"{FONT_DIR}/DejaVuSans.ttf", 14),
        "footer": PilFont.truetype(f"{FONT_DIR}/DejaVuSans.ttf", 15),
    }


def text_block(draw, x, y, text, face, fill, width, leading):
    """Draw text wrapped to width; return the y below its last line."""
    words = text.split()
    lines = []
    current = ""
    for word in words:
        trial = word if not current else f"{current} {word}"
        if draw.textlength(trial, font=face) <= width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    for line in lines:
        draw.text((x, y), line, font=face, fill=fill)
        y += leading
    return y


def tracked_centre(draw, cx, y, text, face, fill, tracking):
    """Draw text centred on cx with extra space between letters."""
    widths = [draw.textlength(ch, font=face) for ch in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x = cx - total / 2
    for ch, w in zip(text, widths):
        draw.text((x, y), ch, font=face, fill=fill)
        x += w + tracking


def fit_cover(image, width, height):
    """Scale and centre-crop an image so it exactly covers width x height."""
    iw, ih = image.size
    scale = max(width / iw, height / ih)
    grown = image.resize(
        (round(iw * scale), round(ih * scale)), PilImage.LANCZOS
    )
    left = (grown.width - width) // 2
    top = (grown.height - height) // 2
    return grown.crop((left, top, left + width, top + height))


STORIES = [
    {
        "kicker": "EUROPE \u00b7 NATO",
        "head": "Russian missiles land in Poland",
        "deck": "NATO calls it a violation as Europe held military drills nearby.",
    },
    {
        "kicker": "ASIA \u00b7 SUMMIT",
        "head": "Trump, Xi and Putin talk nukes, no breakthrough",
        "deck": "Rare three-way talks on nuclear risks end with no deal.",
    },
    {
        "kicker": "MIDDLE EAST",
        "head": "Houthis launch revenge strikes on Saudi capital",
        "deck": "Strikes hit Riyadh as Gulf tensions climb again.",
    },
    {
        "kicker": "CLIMATE \u00b7 COP31",
        "head": "COP31 reaches final day, deal still short",
        "deck": "Countries demand a stronger climate deal in Antalya.",
    },
]

BRIEFS = [
    {
        "head": "Brazil town clears rubble after deadly storm",
        "deck": "\u201cWe lost everything,\u201d residents say after the storm.",
    },
    {
        "head": "6.7-magnitude quake hits Peru",
        "deck": "No deaths reported after the strong tremor.",
    },
    {
        "head": "Nvidia faces US accounting probe",
        "deck": "Shares under pressure amid deepening turmoil.",
    },
    {
        "head": "Rohingyas hail genocide verdict on Myanmar",
        "deck": "World court ruling welcomed after years of waiting.",
    },
]


def draw_story(draw, fonts, x, y, story):
    """Draw one main story cell; return the y below its deck."""
    draw.text((x, y), story["kicker"], font=fonts["kicker"], fill=ALERT_RED)
    y = text_block(
        draw, x, y + 24, story["head"], fonts["headline"], BODY_INK,
        COL_W, 36,
    )
    return text_block(
        draw, x, y + 4, story["deck"], fonts["deck"], MUTED, COL_W, 22
    )


def draw_brief(draw, fonts, x, y, brief):
    """Draw one brief cell; return the y below its deck."""
    draw.text((x, y), "\u2022", font=fonts["brief_head"], fill=BODY_INK)
    y = text_block(
        draw, x + 22, y, brief["head"], fonts["brief_head"], BODY_INK,
        COL_W - 22, 20,
    )
    return text_block(
        draw, x + 22, y + 2, brief["deck"], fonts["brief_deck"], MUTED,
        COL_W - 22, 18,
    )


def build_page():
    """Compose the whole front page and return the image."""
    fonts = load_fonts()
    page = PilImage.new("RGB", (PAGE_W, PAGE_H), PAPER)
    draw = PilDraw.Draw(page)

    draw.rectangle([0, 0, PAGE_W, MASTHEAD_H], fill=NAVY_INK)
    draw.text(
        (PAGE_W / 2, 22), "THE WORLD IN ONE DAY", font=fonts["masthead"],
        fill=WHITE, anchor="ma",
    )
    tracked_centre(
        draw, PAGE_W / 2, 84, "SUNDAY, 22 NOVEMBER 2026",
        fonts["date"], GOLD_LINE, 5,
    )
    draw.rectangle([0, MASTHEAD_H, PAGE_W, MASTHEAD_H + 4], fill=GOLD_LINE)

    here = os.path.dirname(os.path.abspath(__file__))
    hero = PilImage.open(os.path.join(here, "hero.png")).convert("RGB")
    page.paste(fit_cover(hero, PAGE_W, HERO_H), (0, MASTHEAD_H + 4))

    xs = [MARGIN, MARGIN + 500]
    y = MASTHEAD_H + 4 + HERO_H + 24
    row_bottom = max(
        draw_story(draw, fonts, xs[0], y, STORIES[0]),
        draw_story(draw, fonts, xs[1], y, STORIES[1]),
    )
    draw.line([(GUTTER, y), (GUTTER, row_bottom)], fill=HAIRLINE, width=1)
    draw.line(
        [(MARGIN, row_bottom + 10), (PAGE_W - MARGIN, row_bottom + 10)],
        fill=HAIRLINE, width=1,
    )
    y = row_bottom + 22
    row_bottom = max(
        draw_story(draw, fonts, xs[0], y, STORIES[2]),
        draw_story(draw, fonts, xs[1], y, STORIES[3]),
    )
    draw.line([(GUTTER, y), (GUTTER, row_bottom)], fill=HAIRLINE, width=1)

    draw.rectangle(
        [MARGIN, row_bottom + 12, PAGE_W - MARGIN, row_bottom + 15],
        fill=NAVY_INK,
    )
    y = row_bottom + 26
    draw.text((MARGIN, y), "IN BRIEF", font=fonts["section"], fill=NAVY_INK)
    y += 30
    first_row = max(
        draw_brief(draw, fonts, xs[0], y, BRIEFS[0]),
        draw_brief(draw, fonts, xs[1], y, BRIEFS[1]),
    )
    y = first_row + 12
    draw_brief(draw, fonts, xs[0], y, BRIEFS[2])
    draw_brief(draw, fonts, xs[1], y, BRIEFS[3])

    draw.text(
        (PAGE_W / 2, 988),
        "All stories checked against news reports dated 22 November 2026 "
        "\u00b7 make.fun news-image-20261122",
        font=fonts["footer"], fill=MUTED, anchor="ma",
    )
    return page


if __name__ == "__main__":
    out_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "entry.png"
    )
    build_page().save(out_path, optimize=True)
    print("wrote", out_path)
