#!/usr/bin/env python3
"""Render the MNJ lineup as 1280x720 PNG frames for the Pi framebuffer kiosk.

Each day gets a folder of frames; across frames a random subset of DJ names is
dimmed to fake the faulty-neon blink. fbi cycles the frames on the Pi.
"""

import os
import random
from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont

random.seed(2026)

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
FONT_PATH = os.path.join(ROOT, "assets", "fonts", "ScribbleWire.ttf")
OUT = os.path.join(ROOT, "kiosk_frames")

W, H = 1280, 720
BG = (25, 242, 2)            # #19f202
MONSTER = (198, 0, 237)      # #c600ed
DJ_COLORS = {
    "blue": (32, 68, 232),       # #2044e8
    "red": (241, 13, 27),        # #f10d1b
    "yellow": (246, 235, 2),     # #f6eb02
    "lightblue": (2, 247, 222),  # #02f7de
}
DJ_ORDER = ["blue", "red", "yellow", "lightblue"]

# Dimmed = the "off" half of the neon flicker. Multiply toward bg green.
def dim(color, f=0.45):
    return tuple(round(c * f + b * (1 - f)) for c, b in zip(color, BG))

LINEUPS = {
    1: [
        ("22:00 - 00:00", "Emanuelle"),
        ("00:00 - 03:00", "João Comazzi"),
        ("03:00 - 06:00", "Oph"),
    ],
    2: [
        ("22:00 - 00:00", "Elkï"),
        ("00:00 - 03:00", "Panamoil"),
        ("03:00 - 06:00", "Jo"),
        ("06:00 - 09:00", "Chami"),
        ("10:00 - 13:00", "Minijob"),
    ],
}

FRAMES_PER_DAY = 6
TIME_SIZE = 40
DJ_SIZE = 52
ROW_GAP = 22
COL_GAP = 44
TOP_BIAS = 24  # slight downward bias
SIDE_MARGIN = 40  # keep the whole block this far from screen edges

# Monsters scaled down to frame the corners without crowding the text.
m1 = Image.open("/tmp/monster1_big.png").convert("RGBA")  # bottom-left
m2 = Image.open("/tmp/monster2_big.png").convert("RGBA")  # top-right
m1 = m1.resize((int(m1.width * 0.62), int(m1.height * 0.62)), Image.LANCZOS)
m2 = m2.resize((int(m2.width * 0.5), int(m2.height * 0.5)), Image.LANCZOS)


# Fallback font for glyphs ScribbleWire lacks (accents like ã, ï).
FALLBACK_PATH = "/System/Library/Fonts/Supplemental/Arial.ttf"

# Which codepoints does ScribbleWire actually contain?
_SCRIBBLE_CMAP = set(TTFont(FONT_PATH).getBestCmap().keys())


def has_glyph(ch):
    return ord(ch) in _SCRIBBLE_CMAP


def load_font(size):
    return ImageFont.truetype(FONT_PATH, size)


def load_fallback(size):
    return ImageFont.truetype(FALLBACK_PATH, size)


def runs(txt):
    """Split text into (string, uses_fallback) runs by glyph availability."""
    out = []
    for ch in txt:
        fb = not has_glyph(ch)
        if out and out[-1][1] == fb:
            out[-1] = (out[-1][0] + ch, fb)
        else:
            out.append((ch, fb))
    return out


def measure(draw, txt, scribble, fallback):
    """Total advance width and max ascent/descent for mixed-font text."""
    w = 0
    top = 0
    bot = 0
    for s, fb in runs(txt):
        font = fallback if fb else scribble
        b = draw.textbbox((0, 0), s, font=font)
        w += draw.textlength(s, font=font)
        top = min(top, b[1])
        bot = max(bot, b[3])
    return int(w), top, bot


def draw_mixed(draw, xy, txt, scribble, fallback, fill):
    """Draw text left-to-right switching to the fallback font per glyph run."""
    x, y = xy
    for s, fb in runs(txt):
        font = fallback if fb else scribble
        draw.text((x, y), s, font=font, fill=fill)
        x += draw.textlength(s, font=font)


def text_size(draw, txt, font):
    b = draw.textbbox((0, 0), txt, font=font)
    return b[2] - b[0], b[3] - b[1]


def render_frame(day, frame_idx):
    img = Image.new("RGB", (W, H), BG)

    # Monsters first (behind text). monster2 top-right, monster1 bottom-left.
    img.paste(m2, (W - m2.width + 10, -10), m2)
    img.paste(m1, (-20, H - m1.height + 20), m1)

    draw = ImageDraw.Draw(img)
    slots = LINEUPS[day]

    # The lineup block must fit between the bottom-left monster and the right
    # margin, so the available width excludes the monster's footprint.
    LEFT_GUARD = m1.width + 20
    avail_w = W - SIDE_MARGIN - LEFT_GUARD

    # Shrink fonts until the widest row fits that available width.
    time_size, dj_size = TIME_SIZE, DJ_SIZE
    while True:
        time_font = load_font(time_size)
        time_fb = load_fallback(time_size)
        dj_font = load_font(dj_size)
        dj_fb = load_fallback(dj_size)
        time_w_max = max(measure(draw, t, time_font, time_fb)[0] for t, _ in slots)
        dj_w_max = max(measure(draw, d, dj_font, dj_fb)[0] for _, d in slots)
        block_w = time_w_max + COL_GAP + dj_w_max
        if block_w <= avail_w or dj_size <= 28:
            break
        time_size -= 2
        dj_size -= 2

    row_heights = []
    for t, d in slots:
        _, tt, tb = measure(draw, t, time_font, time_fb)
        _, dt, db = measure(draw, d, dj_font, dj_fb)
        row_heights.append(max(tb - tt, db - dt))

    total_h = sum(row_heights) + ROW_GAP * (len(slots) - 1)
    start_y = (H - total_h) // 2 + TOP_BIAS

    # Center the block within the guarded area (right of the monster).
    block_x = LEFT_GUARD + (avail_w - block_w) // 2
    time_right_x = block_x + time_w_max
    dj_left_x = block_x + time_w_max + COL_GAP

    # Which names are "off" this frame (random per-name flicker).
    n = len(slots)
    if frame_idx == 0:
        off = set()  # one clean all-on frame
    else:
        k = random.randint(1, max(1, n // 2))
        off = set(random.sample(range(n), k))

    y = start_y
    for i, (t, d) in enumerate(slots):
        rh = row_heights[i]
        tw, tt, tbot = measure(draw, t, time_font, time_fb)
        # time (purple, right-aligned); subtract bbox top so baseline aligns
        draw_mixed(draw, (time_right_x - tw, y - tt + (rh - (tbot - tt)) // 2),
                   t, time_font, time_fb, MONSTER)
        # dj name (cycling color, left-aligned), dimmed if off this frame
        color = DJ_COLORS[DJ_ORDER[i % len(DJ_ORDER)]]
        if i in off:
            color = dim(color)
        dw, dt, dbot = measure(draw, d, dj_font, dj_fb)
        draw_mixed(draw, (dj_left_x, y - dt + (rh - (dbot - dt)) // 2),
                   d, dj_font, dj_fb, color)
        y += rh + ROW_GAP

    return img


def main():
    for day in (1, 2):
        d = os.path.join(OUT, f"day{day}")
        os.makedirs(d, exist_ok=True)
        for f in range(FRAMES_PER_DAY):
            img = render_frame(day, f)
            img.save(os.path.join(d, f"frame{f:02d}.png"))
        print(f"day{day}: {FRAMES_PER_DAY} frames -> {d}")


if __name__ == "__main__":
    main()
