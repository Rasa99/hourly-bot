# Hourly Trading Bot

**Updated 2026-08-29 12:12 UTC** &nbsp;·&nbsp; refreshes itself every hour

Paper money. $20 simulated, real Gate.io prices, no API keys — it cannot place a real order.

## Money

| | |
|---|---|
| **Equity now** | **$19.8864** 🔴 -0.57% |
| Settled balance | $19.8584 (-0.71%) |
| Unrealised (open trades) | 🟢 +0.0280 |
| Started with | $20.0000 |
| Finished trades | 1 |
| Open now | 4 |
| Win rate | 0% (0/1) |

![balance](chart-equity.svg)

## Open right now

| Coin | Direction | Entry | Price now | Moved | P&L | on margin | Room to stop |
|---|---|---|---|---|---|---|---|
| **FIL** | SHORT 🔻 | 0.6813 | 0.6776 | -0.54% | 🟢 +0.0385 | +5.4% | 3.28% |
| **SAND** | SHORT 🔻 | 0.03898 | 0.03925 | +0.69% | 🔴 -0.0486 | -6.9% | 2.01% |
| **AXS** | SHORT 🔻 | 0.895 | 0.8909 | -0.46% | 🟢 +0.0353 | +4.6% | 2.95% |
| **BCH** | SHORT 🔻 | 243.04 | 242.97 | -0.03% | 🟢 +0.0028 | +0.3% | 1.87% |
| | | | | **total** | **+0.0280** | | |

> ⚠️ **All 4 positions are short.** That is one bet on the same market direction, placed 4 times — these coins move together, so they will win together and lose together. Gross exposure is **159% of equity**.

![FIL](pos-FIL.png)

![SAND](pos-SAND.png)

![AXS](pos-AXS.png)

![BCH](pos-BCH.png)


## What it is waiting for

**0 coin(s) ready to fire right now.** Scanned 47 coins.

![closest to entry](chart-closest.svg)

![what is blocking entries](chart-blockers.svg)

| Coin | Would be | Needs | Status |
|---|---|---|---|
| SNX | SHORT | 0.00% | volume below average |
| IOTA | SHORT | 0.18% | needs 0.2% move; volume below average |
| ALGO | SHORT | 0.22% | needs 0.2% move; volume below average |
| ADA | SHORT | 0.45% | needs 0.5% move; volume below average |
| ENJ | SHORT | 1.01% | needs 1.0% move; volume below average |
| ICP | LONG | 1.34% | needs 1.3% move; volume below average |
| AXS | SHORT | 1.50% | needs 1.5% move; volume below average |
| FIL | SHORT | 1.61% | needs 1.6% move; volume below average |
| RVN | SHORT | 1.73% | needs 1.7% move; trend too weak (ADX 14/20) |
| LRC | SHORT | 2.57% | needs 2.6% move; volume below average |

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
