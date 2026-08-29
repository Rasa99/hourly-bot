# Hourly Trading Bot

**Updated 2026-08-29 15:12 UTC** &nbsp;·&nbsp; refreshes itself every hour

Paper money. $20 simulated, real Gate.io prices, no API keys — it cannot place a real order.

## Money

| | |
|---|---|
| **Equity now** | **$19.7671** 🔴 -1.16% |
| Settled balance | $19.8584 (-0.71%) |
| Unrealised (open trades) | 🔴 -0.0913 |
| Started with | $20.0000 |
| Finished trades | 1 |
| Open now | 5 |
| Win rate | 0% (0/1) |

![balance](chart-equity.svg)

## Open right now

| Coin | Direction | Entry | Price now | Moved | P&L | on margin | Room to stop |
|---|---|---|---|---|---|---|---|
| **FIL** | SHORT 🔻 | 0.6813 | 0.6831 | +0.26% | 🔴 -0.0187 | -2.6% | 2.44% |
| **SAND** | SHORT 🔻 | 0.03898 | 0.03841 | -1.46% | 🟢 +0.1026 | +14.6% | 4.24% |
| **AXS** | SHORT 🔻 | 0.895 | 0.9031 | +0.91% | 🔴 -0.0697 | -9.1% | 1.56% |
| **BCH** | SHORT 🔻 | 243.04 | 246.26 | +1.32% | 🔴 -0.1288 | -13.2% | 0.50% |
| **ICP** | LONG 🔺 | 2.518 | 2.525 | +0.28% | 🟢 +0.0233 | +2.8% | 2.61% |
| | | | | **total** | **-0.0913** | | |

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
| DASH | LONG | 0.02% | needs 0.0% move; volume below average |
| ICP | LONG | 0.20% | needs 0.2% move; volume below average |
| SAND | SHORT | 0.62% | needs 0.6% move; volume below average |
| SNX | SHORT | 0.71% | needs 0.7% move; volume below average |
| IOTA | SHORT | 1.02% | needs 1.0% move; volume below average |
| ADA | SHORT | 1.49% | needs 1.5% move; volume below average |
| BCH | SHORT | 1.53% | needs 1.5% move; volume below average |
| DOT | SHORT | 1.66% | needs 1.7% move |
| ALGO | SHORT | 1.85% | needs 1.9% move; volume below average |
| RVN | SHORT | 1.96% | needs 2.0% move; trend too weak (ADX 13/20) |

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
