# Hourly Trading Bot

**Updated 2026-08-29 18:12 UTC** &nbsp;·&nbsp; refreshes itself every hour

Paper money. $20 simulated, real Gate.io prices, no API keys — it cannot place a real order.

## Money

| | |
|---|---|
| **Equity now** | **$19.8510** 🔴 -0.75% |
| Settled balance | $19.8584 (-0.71%) |
| Unrealised (open trades) | 🔴 -0.0074 |
| Started with | $20.0000 |
| Finished trades | 1 |
| Open now | 5 |
| Win rate | 0% (0/1) |

![balance](chart-equity.svg)

## Open right now

| Coin | Direction | Entry | Price now | Moved | P&L | on margin | Room to stop |
|---|---|---|---|---|---|---|---|
| **FIL** | SHORT 🔻 | 0.6813 | 0.6791 | -0.32% | 🟢 +0.0229 | +3.2% | 3.05% |
| **SAND** | SHORT 🔻 | 0.03898 | 0.03799 | -2.54% | 🟢 +0.1782 | +25.4% | 5.40% |
| **AXS** | SHORT 🔻 | 0.895 | 0.8974 | +0.27% | 🔴 -0.0206 | -2.7% | 2.21% |
| **BCH** | SHORT 🔻 | 243.04 | 245.74 | +1.11% | 🔴 -0.1080 | -11.1% | 0.72% |
| **ICP** | LONG 🔺 | 2.518 | 2.494 | -0.95% | 🔴 -0.0798 | -9.5% | 1.40% |
| | | | | **total** | **-0.0074** | | |

> 1 long / 4 short · gross exposure **201% of equity**.

![FIL](pos-FIL.png)

![SAND](pos-SAND.png)

![AXS](pos-AXS.png)

![BCH](pos-BCH.png)

![ICP](pos-ICP.png)


## What it is waiting for

**0 coin(s) ready to fire right now.** Scanned 47 coins.

![closest to entry](chart-closest.svg)

![what is blocking entries](chart-blockers.svg)

| Coin | Would be | Needs | Status |
|---|---|---|---|
| SNX | SHORT | 0.38% | needs 0.4% move; volume below average |
| DOT | SHORT | 0.60% | needs 0.6% move; volume below average |
| SAND | SHORT | 0.66% | needs 0.7% move; volume below average |
| ADA | SHORT | 0.80% | needs 0.8% move; volume below average |
| DASH | LONG | 1.26% | needs 1.3% move; volume below average |
| BCH | SHORT | 1.28% | needs 1.3% move; volume below average |
| IOTA | SHORT | 1.46% | needs 1.5% move; volume below average |
| ENJ | SHORT | 1.52% | needs 1.5% move; volume below average |
| FIL | SHORT | 1.81% | needs 1.8% move; volume below average |
| ALGO | SHORT | 1.89% | needs 1.9% move; volume below average |

A trade needs **all four** of: price breaking its 3-day range, the trend filter agreeing, enough momentum (ADX over 20), and above-average volume. A coin at 0.00% that still has not traded is being held back by one of the other three — the table says which.

![market backdrop](chart-mood.svg)

## Results

![wins vs losses](chart-winloss.svg)

### Last 15 finished trades

| Coin | Direction | Result | Why it closed | When |
|---|---|---|---|---|
| UNI | LONG | 🔴 -0.1416 (-30.3%) | trailing_stop_loss | 2026-08-28 10:07 |

---

### How it works

Watches 47 coins every hour. Goes long when one breaks above its 3-day high, short when one breaks below its 3-day low — but only if the trend, momentum and volume all agree.

Every trade gets a stop-loss. Winners are left to run on a trailing stop rather than closed at a fixed target. It risks 1% of the account per trade and never holds more than 5 positions on the same side, so one bad day cannot end it.

**It loses more trades than it wins** — about 2-3 winners in 10, by design, with the winners much larger. Backtested on 2024-2026 it lost money. This is running on live prices with fake money to see what it actually does.
