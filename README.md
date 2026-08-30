# Hourly Trading Bot

**Updated 2026-08-30 01:10 UTC** &nbsp;·&nbsp; refreshes itself every hour

Paper money. $20 simulated, real Gate.io prices, no API keys — it cannot place a real order.

## Money

| | |
|---|---|
| **Equity now** | **$19.5393** 🔴 -2.30% |
| Settled balance | $19.6663 (-1.67%) |
| Unrealised (open trades) | 🔴 -0.1270 |
| Started with | $20.0000 |
| Finished trades | 2 |
| Open now | 5 |
| Win rate | 0% (0/2) |

![balance](chart-equity.svg)

## Open right now

| Coin | Direction | Entry | Price now | Moved | P&L | on margin | Room to stop |
|---|---|---|---|---|---|---|---|
| **FIL** | SHORT 🔻 | 0.6813 | 0.6782 | -0.46% | 🟢 +0.0256 | +3.6% | 3.18% |
| **SAND** | SHORT 🔻 | 0.03898 | 0.03846 | -1.33% | 🟢 +0.0493 | +7.0% | 4.11% |
| **AXS** | SHORT 🔻 | 0.895 | 0.9004 | +0.60% | 🔴 -0.0511 | -6.6% | 1.87% |
| **ICP** | LONG 🔺 | 2.518 | 2.466 | -2.07% | 🔴 -0.1830 | -21.8% | 0.28% |
| **EGLD** | LONG 🔺 | 3.622 | 3.64 | +0.50% | 🟢 +0.0322 | +3.9% | 2.72% |
| | | | | **total** | **-0.1270** | | |

> 2 long / 3 short · gross exposure **196% of equity**.

![FIL](pos-FIL.png)

![SAND](pos-SAND.png)

![AXS](pos-AXS.png)

![ICP](pos-ICP.png)

![EGLD](pos-EGLD.png)


## What it is waiting for

**0 coin(s) ready to fire right now.** Scanned 47 coins.

![closest to entry](chart-closest.svg)

![what is blocking entries](chart-blockers.svg)

| Coin | Would be | Needs | Status |
|---|---|---|---|
| EGLD | LONG | 0.00% | volume below average |
| SNX | SHORT | 0.38% | needs 0.4% move; volume below average |
| ADA | SHORT | 0.95% | needs 0.9% move |
| DOT | SHORT | 0.95% | needs 1.0% move; volume below average |
| ENJ | SHORT | 1.52% | needs 1.5% move; volume below average |
| BCH | SHORT | 1.58% | needs 1.6% move; volume below average |
| SAND | SHORT | 1.87% | needs 1.9% move; volume below average |
| LRC | SHORT | 1.97% | needs 2.0% move; volume below average |
| RVN | SHORT | 2.00% | needs 2.0% move; trend too weak (ADX 13/20) |
| FIL | SHORT | 2.04% | needs 2.0% move; volume below average |

A trade needs **all four** of: price breaking its 3-day range, the trend filter agreeing, enough momentum (ADX over 20), and above-average volume. A coin at 0.00% that still has not traded is being held back by one of the other three — the table says which.

![market backdrop](chart-mood.svg)

## Results

![wins vs losses](chart-winloss.svg)

### Last 15 finished trades

| Coin | Direction | Result | Why it closed | When |
|---|---|---|---|---|
| BCH | SHORT | 🔴 -0.1922 (-19.8%) | trailing_stop_loss | 2026-08-29 20:06 |
| UNI | LONG | 🔴 -0.1416 (-30.3%) | trailing_stop_loss | 2026-08-28 10:07 |

---

### How it works

Watches 47 coins every hour. Goes long when one breaks above its 3-day high, short when one breaks below its 3-day low — but only if the trend, momentum and volume all agree.

Every trade gets a stop-loss. Winners are left to run on a trailing stop rather than closed at a fixed target. It risks 1% of the account per trade and never holds more than 5 positions on the same side, so one bad day cannot end it.

**It loses more trades than it wins** — about 2-3 winners in 10, by design, with the winners much larger. Backtested on 2024-2026 it lost money. This is running on live prices with fake money to see what it actually does.
