/* MNJ 2026 — inside dancefloor lineup.
   Fixed for a 1280x720 CRT running Chromium kiosk on a Pi. */

const LINEUPS = {
  1: {
    label: 'Day One',
    slots: [
      { day: 'Friday',   start: '22:00', end: '23:00', dj: 'Emanuelle' },
      { day: 'Friday',   start: '23:00', end: '00:00', dj: 'Emanuelle' },
      { day: 'Saturday', start: '00:00', end: '03:00', dj: 'João Comazzi' },
      { day: 'Saturday', start: '03:00', end: '06:00', dj: 'Oph' },
    ],
  },
  2: {
    label: 'Day Two',
    slots: [
      { day: 'Saturday', start: '22:00', end: '00:00', dj: 'Elkï' },
      { day: 'Sunday',   start: '00:00', end: '03:00', dj: 'Panamoil' },
      { day: 'Sunday',   start: '03:00', end: '06:00', dj: 'Jo' },
      { day: 'Sunday',   start: '06:00', end: '09:00', dj: 'Chami' },
      { day: 'Sunday',   start: '10:00', end: '13:00', dj: 'Minijob' },
    ],
  },
};

/* Pick the day. Override priority (highest first):
     1. ?day=1 / ?day=2 in the URL
     2. a saved choice from pressing the 1 / 2 keys (localStorage)
   Otherwise fall back to the date: shift the clock back 8h so a party
   that runs past midnight still counts as the night it started on.
     Fri Jun 26  -> Day One
     Sat Jun 27  -> Day Two
   Anything earlier defaults to Day One, anything later to Day Two. */
function pickDay() {
  const urlDay = new URLSearchParams(location.search).get('day');
  if (urlDay === '1' || urlDay === '2') return Number(urlDay);

  const saved = localStorage.getItem('mnjDay');
  if (saved === '1' || saved === '2') return Number(saved);

  const now = new Date();
  const shifted = new Date(now.getTime() - 8 * 60 * 60 * 1000);
  const y = shifted.getFullYear();
  const m = shifted.getMonth(); // 0-indexed: June = 5
  const d = shifted.getDate();

  // Day Two starts on Sat Jun 27, 2026 (after the 8h shift).
  if (y > 2026) return 2;
  if (y === 2026 && m > 5) return 2;
  if (y === 2026 && m === 5 && d >= 27) return 2;
  return 1;
}

const DJ_COLORS = ['blue', 'red', 'yellow', 'lightblue'];

function render() {
  const day = pickDay();
  const data = LINEUPS[day];

  document.body.classList.add(`is-day-${day}`);

  const list = document.getElementById('lineupList');
  list.innerHTML = '';

  data.slots.forEach((slot, i) => {
    const li = document.createElement('li');
    li.className = 'lineup__slot';

    const time = document.createElement('span');
    time.className = 'lineup__time';
    time.textContent = `${slot.start} - ${slot.end}`;

    const name = document.createElement('span');
    name.className = 'lineup__dj';
    name.textContent = slot.dj;
    name.dataset.color = DJ_COLORS[i % DJ_COLORS.length];
    // Randomize each name's flicker so they don't blink in unison.
    const dur = 2.4 + Math.random() * 3.2;   // 2.4s – 5.6s cycle
    const delay = Math.random() * dur;        // desync start within its cycle
    name.style.animationDuration = `${dur.toFixed(2)}s`;
    name.style.animationDelay = `-${delay.toFixed(2)}s`;

    li.append(time, name);
    list.appendChild(li);
  });
}

document.addEventListener('DOMContentLoaded', render);

/* Manual toggle: press 1 or 2 to force a day (saved across reloads),
   press 0 to clear and go back to date-based auto-pick. */
document.addEventListener('keydown', (e) => {
  if (e.key === '1' || e.key === '2') {
    localStorage.setItem('mnjDay', e.key);
    location.reload();
  } else if (e.key === '0') {
    localStorage.removeItem('mnjDay');
    location.reload();
  }
});
