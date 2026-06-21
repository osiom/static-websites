#!/usr/bin/env python3
"""Render the MNJ lineup as 1280x720 PNG frames for the Pi framebuffer kiosk.

Each day gets a folder of frames; across frames a random subset of DJ names is
dimmed to fake the faulty-neon blink. fbi cycles the frames on the Pi.
"""

import argparse
import os
import random
from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont

random.seed(2026)

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
FONT_PATH = os.path.join(ROOT, "assets", "fonts", "ScribbleWire.ttf")

# HDMI (720p) vs PAL composite for the CRT. Composite is 720x576 but a CRT
# overscans, so we draw the whole scene inside a safe inset and never near the
# physical edge. Output dirs are separate so both sets can ship together.
# mscale shrinks the monsters relative to their nominal width fraction. On the
# small 720px composite canvas the full-size monsters left only ~240px for the
# lineup (too narrow for "João Comazzi"), so they're scaled down there.
#
# PAL framebuffer is always 720x576, but a 4:3 tube stretches those pixels
# vertically (non-square pixels). We still render a 720x576 PNG (that's what the
# framebuffer is), and sdtv_aspect=2 tells the firmware to present it 4:3. The
# layout adapts via the H-relative fractions, so it stays balanced on the tube.
MODES = {
    "hdmi": dict(W=1280, H=720, out="kiosk_frames", inset=0, mscale=1.0),
    "composite": dict(W=720, H=576, out="kiosk_frames_pal", inset=48, mscale=1.4),
}
BG = (25, 242, 2)            # #19f202
MONSTER = (198, 0, 237)      # #c600ed
# Times are cyan, not purple: purple times vanished where they crossed the
# (now larger, overlapping) purple monsters. Cyan pops on both green and purple.
TIME_COLOR = (2, 247, 222)   # #02f7de
DJ_COLORS = {
    "blue": (32, 68, 232),       # #2044e8
    "red": (241, 13, 27),        # #f10d1b
    "yellow": (246, 235, 2),     # #f6eb02
    "lightblue": (2, 247, 222),  # #02f7de
}
# lightblue (cyan) is reserved for the time text now, so it's out of the name
# cycle to avoid name/time color clashes.
DJ_ORDER = ["blue", "red", "yellow"]

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
# Type/spacing as a fraction of canvas height so both resolutions look alike.
TIME_FRAC = 46 / 720
DJ_FRAC = 60 / 720
ROW_GAP_FRAC = 22 / 720
COL_GAP_FRAC = 44 / 1280
TOP_BIAS_FRAC = 24 / 720

# Monster footprint as a fraction of canvas width. The old 1280-wide frames used
# 0.62*460=285px (bottom-left) and 0.5*720=360px (top-right); keep those ratios.
M1_WFRAC = 0.62 * 460 / 1280  # bottom-left, ~0.223 of width
M2_WFRAC = 0.5 * 720 / 1280   # top-right, ~0.281 of width

_m1_src = Image.open("/tmp/monster1_big.png").convert("RGBA")  # bottom-left
_m2_src = Image.open("/tmp/monster2_big.png").convert("RGBA")  # top-right


def scale_to_width(img, target_w):
    f = target_w / img.width
    return img.resize((int(img.width * f), int(img.height * f)), Image.LANCZOS)


# Fallback font for glyphs ScribbleWire lacks (accents like ã, ï).
FALLBACK_PATH = "/System/Library/Fonts/Supplemental/Arial.ttf"

# Which codepoints does ScribbleWire actually contain?
_SCRIBBLE_CMAP = set(TTFont(FONT_PATH).getBestCmap().keys())


def has_glyph(ch):
    return ord(ch) in _SCRIBBLE_CMAP


def load_font(size):
    return ImageFont.truetype(FONT_PATH, size)


# ScribbleWire's hand-drawn caps are much taller than Arial at the same point
# size, so an accented glyph borrowed from Arial looks like a shrunken
# superscript. Oversize the fallback so its cap-height roughly matches.
FALLBACK_SCALE = 1.5


def load_fallback(size):
    return ImageFont.truetype(FALLBACK_PATH, round(size * FALLBACK_SCALE))


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
    """Width and baseline-relative top/bottom for mixed-font text.

    top/bot are measured from the shared baseline (anchor 'ls'), so glyphs from
    different fonts line up on one baseline instead of by their bbox tops.
    """
    w = 0
    top = 0
    bot = 0
    for s, fb in runs(txt):
        font = fallback if fb else scribble
        b = draw.textbbox((0, 0), s, font=font, anchor="ls")
        w += draw.textlength(s, font=font)
        top = min(top, b[1])
        bot = max(bot, b[3])
    return int(w), top, bot


def draw_mixed(draw, xy, txt, scribble, fallback, fill, bold=0):
    """Draw left-to-right switching fonts per run, all on one baseline.

    xy is the left end of the baseline (anchor 'ls'). bold > 0 thickens the
    strokes (faux-bold via stroke_width) since the font has no bold weight.
    """
    x, y = xy
    for s, fb in runs(txt):
        font = fallback if fb else scribble
        draw.text((x, y), s, font=font, fill=fill, anchor="ls",
                  stroke_width=bold, stroke_fill=fill)
        x += draw.textlength(s, font=font)


def render_frame(cfg, m1, m2, day, frame_idx):
    W, H, inset = cfg["W"], cfg["H"], cfg["inset"]
    img = Image.new("RGB", (W, H), BG)

    # Monsters first (behind text). monster2 top-right, monster1 bottom-left.
    # On composite they hug the safe inset, not the physical (overscanned) edge.
    img.paste(m2, (W - m2.width - inset, inset), m2)
    img.paste(m1, (inset, H - m1.height - inset), m1)

    draw = ImageDraw.Draw(img)
    slots = LINEUPS[day]

    COL_GAP = round(COL_GAP_FRAC * W)
    ROW_GAP = round(ROW_GAP_FRAC * H)
    TOP_BIAS = round(TOP_BIAS_FRAC * H)
    min_dj = round(DJ_FRAC * H * 0.54)  # don't shrink below ~54% of nominal

    # Monsters are big and decorative now and may sit BEHIND the text; the names
    # use colors that pop on purple, so we no longer guard against them. The
    # lineup just centers in the full width inside the safe inset.
    pad = round(20 / 1280 * W)
    LEFT_GUARD = inset + pad
    avail_w = W - 2 * (inset + pad)

    # Shrink fonts until the widest row fits that available width.
    time_size, dj_size = round(TIME_FRAC * H), round(DJ_FRAC * H)
    while True:
        time_font = load_font(time_size)
        time_fb = load_fallback(time_size)
        dj_font = load_font(dj_size)
        dj_fb = load_fallback(dj_size)
        time_w_max = max(measure(draw, t, time_font, time_fb)[0] for t, _ in slots)
        dj_w_max = max(measure(draw, d, dj_font, dj_fb)[0] for _, d in slots)
        block_w = time_w_max + COL_GAP + dj_w_max
        if block_w <= avail_w or dj_size <= min_dj:
            break
        time_size -= 2
        dj_size -= 2

    # Faux-bold stroke width, proportional to each font size (min 1px).
    time_bold = max(1, round(time_size * 0.045))
    dj_bold = max(1, round(dj_size * 0.045))

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
        # time (purple, right-aligned); place on a baseline centered in the row.
        t_base = y + (rh - (tbot - tt)) // 2 - tt
        draw_mixed(draw, (time_right_x - tw, t_base),
                   t, time_font, time_fb, TIME_COLOR, bold=time_bold)
        # dj name (cycling color, left-aligned), dimmed if off this frame
        color = DJ_COLORS[DJ_ORDER[i % len(DJ_ORDER)]]
        if i in off:
            color = dim(color)
        dw, dt, dbot = measure(draw, d, dj_font, dj_fb)
        d_base = y + (rh - (dbot - dt)) // 2 - dt
        draw_mixed(draw, (dj_left_x, d_base),
                   d, dj_font, dj_fb, color, bold=dj_bold)
        y += rh + ROW_GAP

    return img


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=MODES, default="hdmi",
                    help="hdmi (1280x720) or composite (720x576 PAL, overscan-safe)")
    args = ap.parse_args()
    cfg = MODES[args.mode]
    W = cfg["W"]

    ms = cfg["mscale"]
    m1 = scale_to_width(_m1_src, round(M1_WFRAC * W * ms))
    m2 = scale_to_width(_m2_src, round(M2_WFRAC * W * ms))

    out = os.path.join(ROOT, cfg["out"])
    for day in (1, 2):
        d = os.path.join(out, f"day{day}")
        os.makedirs(d, exist_ok=True)
        for f in range(FRAMES_PER_DAY):
            img = render_frame(cfg, m1, m2, day, f)
            img.save(os.path.join(d, f"frame{f:02d}.png"))
        print(f"[{args.mode}] day{day}: {FRAMES_PER_DAY} frames "
              f"({cfg['W']}x{cfg['H']}) -> {d}")


if __name__ == "__main__":
    main()
