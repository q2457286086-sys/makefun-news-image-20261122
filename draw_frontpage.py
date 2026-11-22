#!/usr/bin/env python3
"""Draw the 22 November 2026 front page: one 1024x1024 PNG.

Layout, top to bottom: navy masthead, gold rule, hero photo, a 2x2 grid of
main stories, a navy rule, an IN BRIEF block (2x2), and a footer line.
All headlines were verified against news reports dated 22 November 2026.
Run from the repo root:  python3 draw_frontpage.py  ->  entry.png
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BASE = os.path.dirname(os.path.abspath(__file__))

CREAM = (246, 241, 231)
NAVY = (27, 47, 74)
GOLD = (201, 162, 39)
RED = (176, 30, 30)
INK = (26, 26, 26)
GREY = (85, 85, 85)
FAINT = (170, 165, 155)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, fill, max_w, leading):
    """Draw wrapped text; returns the y just below the last line."""
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def tracked(draw, cx, y, text, fnt, fill, tracking):
    """Draw centred text with extra space between letters."""
    widths = [draw.textlength(ch, font=fnt) for ch in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x = cx - total / 2
    for ch, w in zip(text, widths):
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += w + tracking
    return total


def cover(im, w, h):
    """Resize + centre-crop so the image exactly covers w x h."""
    iw, ih = im.size
    scale = max(w / iw, h / ih)
    im = im.resize((round(iw * scale), round(ih * scale)), Image.LANCZOS)
    left = (im.width - w) // 2
    top = (im.height - h) // 2
    return im.crop((left, top, left + w, top + h))


MAIN = [
    ("EUROPE \u00b7 NATO", "Russian missiles land in Poland",
     "NATO calls it a violation as Europe held military drills nearby."),
    ("ASIA \u00b7 SUMMIT", "Trump, Xi and Putin talk nukes, no breakthrough",
     "Rare three-way talks on nuclear risks end with no deal."),
    ("MIDDLE EAST", "Houthis launch revenge strikes on Saudi capital",
     "Strikes hit Riyadh as Gulf tensions climb again."),
    ("CLIMATE \u00b7 COP31", "COP31 reaches final day, deal still short",
     "Countries demand a stronger climate deal in Antalya."),
]

BRIEFS = [
    ("Brazil town clears rubble after deadly storm",
     "\u201cWe lost everything,\u201d residents say after the storm."),
    ("6.7-magnitude quake hits Peru",
     "No deaths reported after the strong tremor."),
    ("Nvidia faces US accounting probe",
     "Shares under pressure amid deepening turmoil."),
    ("Rohingyas hail genocide verdict on Myanmar",
     "World court ruling welcomed after years of waiting."),
]


def story_cell(d, x, y, kicker, head, deck, col_w):
    """Draw one main story; returns the y just below its deck."""
    d.text((x, y), kicker, font=font(SANS_B, 17), fill=RED)
    y = para(d, x, y + 24, head, font(SERIF_B, 30), INK, col_w, 36)
    return para(d, x, y + 4, deck, font(SANS, 17), GREY, col_w, 22)


def brief_cell(d, x, y, title, sub, col_w):
    """Draw one brief; returns the y just below its sub."""
    d.text((x, y), "\u2022", font=font(SANS_B, 16), fill=INK)
    y = para(d, x + 22, y, title, font(SANS_B, 16), INK, col_w - 22, 20)
    return para(d, x + 22, y + 2, sub, font(SANS, 14), GREY, col_w - 22, 18)


def main():
    page = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(page)

    # --- masthead ---
    d.rectangle([0, 0, W, 108], fill=NAVY)
    d.text((W / 2, 22), "THE WORLD IN ONE DAY", font=font(SERIF_B, 62),
           fill=(255, 255, 255), anchor="ma")
    tracked(d, W / 2, 84, "SUNDAY, 22 NOVEMBER 2026", font(SANS_B, 19), GOLD, 5)
    d.rectangle([0, 108, W, 112], fill=GOLD)

    # --- hero photo ---
    hero = Image.open(os.path.join(BASE, "hero.png")).convert("RGB")
    page.paste(cover(hero, W, 260), (0, 112))

    # --- main stories: 2 columns x 2 rows, y flows from real cell bottoms ---
    col_w = 452
    xs = [36, 536]
    y = 396
    row1 = max(story_cell(d, xs[0], y, *MAIN[0], col_w),
               story_cell(d, xs[1], y, *MAIN[1], col_w))
    d.line([(512, y), (512, row1)], fill=FAINT, width=1)
    d.line([(36, row1 + 10), (988, row1 + 10)], fill=FAINT, width=1)
    y = row1 + 22
    row2 = max(story_cell(d, xs[0], y, *MAIN[2], col_w),
               story_cell(d, xs[1], y, *MAIN[3], col_w))
    d.line([(512, y), (512, row2)], fill=FAINT, width=1)

    # --- navy rule + IN BRIEF ---
    d.rectangle([36, row2 + 12, 988, row2 + 15], fill=NAVY)
    y = row2 + 26
    d.text((36, y), "IN BRIEF", font=font(SANS_B, 19), fill=NAVY)
    y += 30
    brow1 = max(brief_cell(d, xs[0], y, *BRIEFS[0], col_w),
                brief_cell(d, xs[1], y, *BRIEFS[1], col_w))
    y = brow1 + 12
    brief_cell(d, xs[0], y, *BRIEFS[2], col_w)
    brief_cell(d, xs[1], y, *BRIEFS[3], col_w)

    # --- footer ---
    d.text((W / 2, 988),
           "All stories checked against news reports dated 22 November 2026 "
           "\u00b7 make.fun news-image-20261122",
           font=font(SANS, 15), fill=GREY, anchor="ma")

    out = os.path.join(BASE, "entry.png")
    page.save(out, optimize=True)
    print("wrote", out)


if __name__ == "__main__":
    main()
