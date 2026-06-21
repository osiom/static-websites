#!/usr/bin/env python3
"""Drive fbi's frame advance for a fast neon flicker.

fbi cycles to the next image when it receives 'j' on its console. fbi reads
from the real console keyboard (not stdin), so we inject the keystroke into
the controlling tty with the TIOCSTI ioctl. Run pointed at the same tty fbi
is on (e.g. /dev/tty1).

    flicker.py <tty> <interval_seconds>
"""

import fcntl
import sys
import termios
import time

TTY = sys.argv[1] if len(sys.argv) > 1 else "/dev/tty1"
INTERVAL = float(sys.argv[2]) if len(sys.argv) > 2 else 0.2

with open(TTY, "w") as t:
    fd = t.fileno()
    while True:
        fcntl.ioctl(fd, termios.TIOCSTI, b"j")
        time.sleep(INTERVAL)
