# Hourly Trading Bot

**Updated 2026-08-29 20:07 UTC** &nbsp;·&nbsp; refreshes itself every hour

Paper money. $20 simulated, real Gate.io prices, no API keys — it cannot place a real order.

## Money

| | |
|---|---|
| **Equity now** | **$19.5588** 🔴 -2.21% |
| Settled balance | $19.6663 (-1.67%) |
| Unrealised (open trades) | 🔴 -0.1074 |
| Started with | $20.0000 |
| Finished trades | 2 |
| Open now | 4 |
| Win rate | 0% (0/2) |

![balance](chart-equity.svg)

## Open right now

| Coin | Direction | Entry | Price now | Moved | P&L | on margin | Room to stop |
|---|---|---|---|---|---|---|---|
| **FIL** | SHORT 🔻 | 0.6813 | 0.6814 | +0.01% | 🔴 -0.0080 | -1.1% | 2.70% |
| **SAND** | SHORT 🔻 | 0.03898 | 0.03875 | -0.59% | 🟢 +0.0119 | +1.7% | 3.33% |
| **AXS** | SHORT 🔻 | 0.895 | 0.9016 | +0.74% | 🔴 -0.0622 | -8.1% | 1.73% |
| **ICP** | LONG 🔺 | 2.518 | 2.506 | -0.48% | 🔴 -0.0491 | -5.9% | 1.88% |
| | | | | **total** | **-0.1074** | | |

> 1 long / 3 short · gross exposure **154% of equity**.

![FIL](pos-FIL.png)

![SAND](pos-SAND.png)

![AXS](pos-AXS.png)

![ICP](pos-ICP.png)


## What it is waiting for

**0 coin(s) ready to fire right now.** Scanned 47 coins.

![closest to entry](chart-closest.svg)

![what is blocking entries](chart-blockers.svg)

| Coin | Would be | Needs | Status |
|---|---|---|---|
| EGLD | LONG | 0.17% | needs 0.2% move; trend too weak (ADX 19/20) |
| SNX | SHORT | 0.38% | needs 0.4% move |
| ADA | SHORT | 1.29% | needs 1.3% move; volume below average |
| DOT | SHORT | 1.31% | needs 1.3% move; volume below average |
| ICP | LONG | 1.40% | needs 1.4% move; volume below average |
| IOTA | SHORT | 1.46% | needs 1.5% move; volume below average |
| ENJ | SHORT | 1.60% | needs 1.6% move |
| RVN | SHORT | 1.79% | needs 1.8% move; trend too weak (ADX 12/20) |
| BCH | SHORT | 1.84% | needs 1.8% move; volume below average |
| FIL | SHORT | 2.01% | needs 2.0% move; volume below average |

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
