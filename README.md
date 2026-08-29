# Hourly Trading Bot

**Updated 2026-08-29 05:12 UTC** &nbsp;·&nbsp; refreshes itself every hour

Paper money. $20 simulated, real Gate.io prices, no API keys — it cannot place a real order.

## Money

| | |
|---|---|
| **Equity now** | **$19.7990** 🔴 -1.01% |
| Settled balance | $19.8584 (-0.71%) |
| Unrealised (open trades) | 🔴 -0.0594 |
| Started with | $20.0000 |
| Finished trades | 1 |
| Open now | 3 |
| Win rate | 0% (0/1) |

![balance](chart-equity.svg)

## Open right now

| Coin | Direction | Entry | Price now | Moved | P&L | on margin | Room to stop |
|---|---|---|---|---|---|---|---|
| **FIL** | SHORT 🔻 | 0.6813 | 0.6859 | +0.68% | 🔴 -0.0479 | -6.8% | 2.03% |
| **SAND** | SHORT 🔻 | 0.03898 | 0.03892 | -0.15% | 🟢 +0.0108 | +1.5% | 2.88% |
| **AXS** | SHORT 🔻 | 0.895 | 0.8976 | +0.29% | 🔴 -0.0224 | -2.9% | 2.18% |
| | | | | **total** | **-0.0594** | | |

> ⚠️ **All 3 positions are short.** That is one bet on the same market direction, placed 3 times — these coins move together, so they will win together and lose together. Gross exposure is **110% of equity**.

![FIL](pos-FIL.png)

![SAND](pos-SAND.png)

![AXS](pos-AXS.png)


## What it is waiting for

**0 coin(s) ready to fire right now.** Scanned 47 coins.

![closest to entry](chart-closest.svg)

![what is blocking entries](chart-blockers.svg)

| Coin | Would be | Needs | Status |
|---|---|---|---|
| LRC | SHORT | 1.12% | needs 1.1% move; volume below average |
| SNX | SHORT | 1.23% | needs 1.2% move; volume below average |
| EGLD | LONG | 1.58% | needs 1.6% move; trend too weak (ADX 20/20) |
| SAND | SHORT | 1.93% | needs 1.9% move; volume below average |
| AXS | SHORT | 2.24% | needs 2.2% move; volume below average |
| ENJ | SHORT | 2.30% | needs 2.3% move; volume below average |
| STORJ | SHORT | 2.49% | needs 2.5% move; volume below average |
| ANKR | LONG | 2.60% | needs 2.6% move; volume below average |
| ICP | LONG | 2.73% | needs 2.7% move; volume below average |
| FIL | SHORT | 2.80% | needs 2.8% move; volume below average |

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
