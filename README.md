# Hourly Trading Bot

**Updated 2026-08-30 02:07 UTC** &nbsp;·&nbsp; refreshes itself every hour

Paper money. $20 simulated, real Gate.io prices, no API keys — it cannot place a real order.

## Money

| | |
|---|---|
| **Equity now** | **$19.6131** 🔴 -1.93% |
| Settled balance | $19.4600 (-2.70%) |
| Unrealised (open trades) | 🟢 +0.1531 |
| Started with | $20.0000 |
| Finished trades | 3 |
| Open now | 5 |
| Win rate | 0% (0/3) |

![balance](chart-equity.svg)

## Open right now

| Coin | Direction | Entry | Price now | Moved | P&L | on margin | Room to stop |
|---|---|---|---|---|---|---|---|
| **FIL** | SHORT 🔻 | 0.6813 | 0.676 | -0.78% | 🟢 +0.0485 | +6.8% | 3.52% |
| **SAND** | SHORT 🔻 | 0.03898 | 0.03838 | -1.54% | 🟢 +0.0637 | +9.1% | 4.33% |
| **AXS** | SHORT 🔻 | 0.895 | 0.8973 | +0.26% | 🔴 -0.0244 | -3.2% | 2.22% |
| **EGLD** | LONG 🔺 | 3.622 | 3.668 | +1.27% | 🟢 +0.0966 | +11.6% | 3.46% |
| **CRV** | SHORT 🔻 | 0.2973 | 0.2981 | +0.27% | 🔴 -0.0312 | -3.1% | 1.61% |
| | | | | **total** | **+0.1531** | | |

> 1 long / 4 short · gross exposure **207% of equity**.

![FIL](pos-FIL.png)

![SAND](pos-SAND.png)

![AXS](pos-AXS.png)

![EGLD](pos-EGLD.png)

![CRV](pos-CRV.png)


## What it is waiting for

**1 coin(s) ready to fire right now.** Scanned 47 coins.

![closest to entry](chart-closest.svg)

![what is blocking entries](chart-blockers.svg)

| Coin | Would be | Needs | Status |
|---|---|---|---|
| EGLD | LONG | 0.00% | **READY** |
| SNX | SHORT | 0.00% | volume below average |
| DOT | SHORT | 0.48% | needs 0.5% move |
| ADA | SHORT | 0.75% | needs 0.7% move |
| RVN | SHORT | 1.11% | needs 1.1% move; trend too weak (ADX 14/20) |
| BCH | SHORT | 1.17% | needs 1.2% move; volume below average |
| FIL | SHORT | 1.45% | needs 1.4% move |
| ENJ | SHORT | 1.48% | needs 1.5% move |
| SAND | SHORT | 1.72% | needs 1.7% move; volume below average |
| LRC | SHORT | 1.85% | needs 1.9% move; volume below average |

A trade needs **all four** of: price breaking its 3-day range, the trend filter agreeing, enough momentum (ADX over 20), and above-average volume. A coin at 0.00% that still has not traded is being held back by one of the other three — the table says which.

![market backdrop](chart-mood.svg)

## Results

![wins vs losses](chart-winloss.svg)

### Last 15 finished trades

| Coin | Direction | Result | Why it closed | When |
|---|---|---|---|---|
| ICP | LONG | 🔴 -0.2062 (-24.6%) | stop_loss | 2026-08-30 01:13 |
| BCH | SHORT | 🔴 -0.1922 (-19.8%) | trailing_stop_loss | 2026-08-29 20:06 |
| UNI | LONG | 🔴 -0.1416 (-30.3%) | trailing_stop_loss | 2026-08-28 10:07 |

---

### How it works

Watches 47 coins every hour. Goes long when one breaks above its 3-day high, short when one breaks below its 3-day low — but only if the trend, momentum and volume all agree.

Every trade gets a stop-loss. Winners are left to run on a trailing stop rather than closed at a fixed target. It risks 1% of the account per trade and never holds more than 5 positions on the same side, so one bad day cannot end it.

**It loses more trades than it wins** — about 2-3 winners in 10, by design, with the winners much larger. Backtested on 2024-2026 it lost money. This is running on live prices with fake money to see what it actually does.
