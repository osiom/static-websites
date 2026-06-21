#!/bin/sh
# MNJ 2026 framebuffer kiosk.
# Picks the day's frame set by date (8h backshift so a party running past
# midnight still counts as the night it started on), preloads the frames in
# fbi, then advances frames fast via stdin to fake the neon blink (fbi's own
# -t timer can't go below 1s; 'j' on stdin = next image).
#
#   Fri Jun 26 2026 -> day1
#   Sat Jun 27 2026 -> day2
# Override: pass 1 or 2 as $1, or set MNJ_DAY=1|2 in the environment.

FRAMES_DIR="${MNJ_FRAMES:-/home/mos/kiosk_frames}"
FLICKER_MS="${MNJ_FLICKER_MS:-200}"   # ms between frame advances

pick_day() {
  if [ "$1" = "1" ] || [ "$1" = "2" ]; then echo "$1"; return; fi
  if [ "$MNJ_DAY" = "1" ] || [ "$MNJ_DAY" = "2" ]; then echo "$MNJ_DAY"; return; fi
  shifted=$(date -d '-8 hours' +%Y%m%d 2>/dev/null) || shifted=$(date +%Y%m%d)
  if [ "$shifted" -ge 20260627 ]; then echo 2; else echo 1; fi
}

DAY=$(pick_day "$1")
DIR="$FRAMES_DIR/day$DAY"

setterm -cursor off 2>/dev/null
printf '\033[?25l'

SLEEP_S=$(awk "BEGIN{printf \"%.3f\", $FLICKER_MS/1000}")

# Feed 'j' (next image) into fbi's stdin forever -> fast frame cycling.
# fbi wraps from the last frame back to the first.
{
  while :; do
    printf 'j'
    sleep "$SLEEP_S"
  done
} | fbi -d /dev/fb0 -T 1 -a --noverbose "$DIR"/frame*.png
