"""
Hand-rolled SVG charts for the status page.

No matplotlib on purpose. This runs inside GitHub Actions every hour, where
every extra dependency is another install to wait for and another thing that
can break the run. SVG is plain text, needs nothing, and GitHub renders it
inline in the README.

Every chart is dark-themed to match GitHub's default and returns the filename
it wrote.
"""

BG = "#0d1117"
FG = "#c9d1d9"
DIM = "#8b949e"
GRID = "#30363d"
GREEN = "#2ea043"
RED = "#f85149"
BLUE = "#388bfd"
AMBER = "#d29922"


def _esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def _write(path, body, w, h):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
           f'viewBox="0 0 {w} {h}">'
           f'<rect width="{w}" height="{h}" fill="{BG}" rx="6"/>{body}</svg>')
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg)
    return path


def _title(t, x=16, y=22):
    return (f'<text x="{x}" y="{y}" fill="{DIM}" font-family="system-ui,sans-serif" '
            f'font-size="12">{_esc(t)}</text>')


# ----------------------------------------------------------------- 1
def equity(closed, start, path="chart-equity.svg"):
    """Balance over time. The one chart that answers 'am I up or down'."""
    W, H, PAD = 720, 210, 34
    bal, run = [start], start
    for r in reversed(closed):
        run += (r["close_profit_abs"] or 0)
        bal.append(run)
    if len(bal) < 2:
        bal = [start, start]

    lo, hi = min(bal), max(bal)
    if hi - lo < 1e-9:
        lo, hi = lo - 0.5, hi + 0.5
    span = hi - lo

    def x(i): return PAD + i * (W - 2 * PAD) / max(len(bal) - 1, 1)
    def y(v): return H - PAD - (v - lo) * (H - 2 * PAD) / span

    pts = " ".join(f"{x(i):.1f},{y(v):.1f}" for i, v in enumerate(bal))
    up = bal[-1] >= start
    col = GREEN if up else RED
    fill = "rgba(46,160,67,.15)" if up else "rgba(248,81,73,.15)"
    sy = y(start)

    body = (
        _title("Balance over time (paper $)")
        + f'<line x1="{PAD}" y1="{sy:.1f}" x2="{W-PAD}" y2="{sy:.1f}" stroke="{GRID}" stroke-dasharray="4 4"/>'
        + f'<polygon points="{PAD},{y(lo):.1f} {pts} {x(len(bal)-1):.1f},{y(lo):.1f}" fill="{fill}"/>'
        + f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="2" stroke-linejoin="round"/>'
        + f'<circle cx="{x(len(bal)-1):.1f}" cy="{y(bal[-1]):.1f}" r="3.5" fill="{col}"/>'
        + f'<text x="{PAD}" y="{H-10}" fill="{DIM}" font-family="system-ui,sans-serif" font-size="11">'
          f'{len(closed)} trades &#183; ${start:.2f} &#8594; ${bal[-1]:.4f}</text>'
    )
    return _write(path, body, W, H)


# ----------------------------------------------------------------- 2
def closest(scan, path="chart-closest.svg", n=10):
    """How far each coin is from triggering. Answers 'what is it waiting for'."""
    W, RH, PAD, TOP = 720, 22, 90, 34
    rows = scan[:n]
    H = TOP + len(rows) * RH + 26
    if not rows:
        return _write(path, _title("No market data"), W, 80)

    worst = max(max(r["gap"] for r in rows), 0.5)
    body = [_title("Closest to triggering a trade (% the price must still move)")]

    for i, r in enumerate(rows):
        y = TOP + i * RH
        bw = (r["gap"] / worst) * (W - PAD - 150)
        ready = r["ready"]
        col = GREEN if ready else (AMBER if r["gap"] < 1 else BLUE)
        body.append(
            f'<text x="12" y="{y+13}" fill="{FG}" font-family="system-ui,sans-serif" '
            f'font-size="12">{_esc(r["coin"])}</text>'
            f'<text x="58" y="{y+13}" fill="{DIM}" font-family="system-ui,sans-serif" '
            f'font-size="10">{_esc(r["side"])}</text>'
            f'<rect x="{PAD}" y="{y+3}" width="{max(bw,2):.1f}" height="13" rx="2" fill="{col}" opacity="0.85"/>'
            f'<text x="{PAD+max(bw,2)+7:.1f}" y="{y+13}" fill="{DIM}" '
            f'font-family="system-ui,sans-serif" font-size="11">'
            f'{r["gap"]:.2f}%{" &#183; READY" if ready else ""}</text>'
        )
    return _write(path, "".join(body), W, H)


# ----------------------------------------------------------------- 3
def blockers(scan, path="chart-blockers.svg"):
    """Why coins that HAVE broken out still are not being traded."""
    W, H = 720, 150
    broke = [r for r in scan if r["gap"] <= 0.01]
    counts = {
        "Ready to fire": sum(1 for r in broke if r["ready"]),
        "Volume too low": sum(1 for r in broke if not r["vol_ok"]),
        "Trend too weak": sum(1 for r in broke if not r["adx_ok"]),
    }
    total = max(sum(counts.values()), 1)
    cols = {"Ready to fire": GREEN, "Volume too low": AMBER, "Trend too weak": RED}

    body = [_title(f"Coins that broke out ({len(broke)}) - and what is holding them back")]
    x = 16
    for label, cnt in counts.items():
        w = max((cnt / total) * (W - 32), 2)
        body.append(
            f'<rect x="{x:.1f}" y="44" width="{w:.1f}" height="26" rx="3" fill="{cols[label]}" opacity="0.85"/>'
            f'<text x="{x:.1f}" y="92" fill="{FG}" font-family="system-ui,sans-serif" font-size="11">'
            f'{_esc(label)}</text>'
            f'<text x="{x:.1f}" y="108" fill="{DIM}" font-family="system-ui,sans-serif" font-size="11">'
            f'{cnt} coin(s)</text>'
        )
        x += w + 8
    if not broke:
        body.append(f'<text x="16" y="60" fill="{DIM}" font-family="system-ui,sans-serif" '
                    f'font-size="12">Nothing has broken out yet - all coins still inside their 3-day range.</text>')
    return _write(path, "".join(body), W, H)


# ----------------------------------------------------------------- 4
def winloss(closed, path="chart-winloss.svg"):
    """Wins vs losses, and the size of each. Shows the shape of the edge."""
    W, H = 720, 160
    wins = [r["close_profit_abs"] for r in closed if (r["close_profit_abs"] or 0) > 0]
    losses = [r["close_profit_abs"] for r in closed if (r["close_profit_abs"] or 0) <= 0]
    body = [_title("Wins vs losses")]

    if not closed:
        body.append(f'<text x="16" y="60" fill="{DIM}" font-family="system-ui,sans-serif" '
                    f'font-size="12">No finished trades yet.</text>')
        return _write(path, "".join(body), W, H)

    aw = sum(wins) / len(wins) if wins else 0
    al = sum(losses) / len(losses) if losses else 0
    wr = len(wins) / len(closed) * 100
    scale = max(abs(aw), abs(al), 0.001)

    body.append(
        f'<text x="16" y="52" fill="{FG}" font-family="system-ui,sans-serif" font-size="13">'
        f'Win rate {wr:.0f}%  ({len(wins)} won / {len(losses)} lost)</text>'
    )
    for i, (lab, val, col) in enumerate(
            [("average win", aw, GREEN), ("average loss", al, RED)]):
        y = 78 + i * 34
        w = max(abs(val) / scale * (W - 260), 2)
        body.append(
            f'<text x="16" y="{y+14}" fill="{DIM}" font-family="system-ui,sans-serif" '
            f'font-size="11">{_esc(lab)}</text>'
            f'<rect x="120" y="{y+2}" width="{w:.1f}" height="16" rx="2" fill="{col}" opacity="0.85"/>'
            f'<text x="{120+w+8:.1f}" y="{y+14}" fill="{FG}" font-family="system-ui,sans-serif" '
            f'font-size="11">{val:+.4f} USDT</text>'
        )
    return _write(path, "".join(body), W, H)


# ----------------------------------------------------------------- 5
def market_mood(scan, path="chart-mood.svg"):
    """How many coins are trending up vs down - the backdrop it is trading in."""
    W, H = 720, 130
    up = sum(1 for r in scan if r["ema_up"])
    dn = len(scan) - up
    strong = sum(1 for r in scan if r["adx_ok"])
    total = max(len(scan), 1)

    uw = up / total * (W - 32)
    body = [
        _title("Market backdrop - coins trending up vs down"),
        f'<rect x="16" y="44" width="{uw:.1f}" height="26" rx="3" fill="{GREEN}" opacity="0.85"/>',
        f'<rect x="{16+uw:.1f}" y="44" width="{(W-32)-uw:.1f}" height="26" rx="3" fill="{RED}" opacity="0.85"/>',
        f'<text x="16" y="90" fill="{FG}" font-family="system-ui,sans-serif" font-size="11">'
        f'{up} trending up</text>',
        f'<text x="{W-16}" y="90" fill="{FG}" font-family="system-ui,sans-serif" font-size="11" '
        f'text-anchor="end">{dn} trending down</text>',
        f'<text x="16" y="110" fill="{DIM}" font-family="system-ui,sans-serif" font-size="11">'
        f'{strong} of {total} have enough momentum to qualify (ADX above 20)</text>',
    ]
    return _write(path, "".join(body), W, H)
