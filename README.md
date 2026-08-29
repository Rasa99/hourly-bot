# Hourly Trading Bot

**Updated 2026-08-29 06:12 UTC** &nbsp;·&nbsp; refreshes itself every hour

Paper money. $20 simulated, real Gate.io prices, no API keys — it cannot place a real order.

## Money

| | |
|---|---|
| **Equity now** | **$19.8016** 🔴 -0.99% |
| Settled balance | $19.8584 (-0.71%) |
| Unrealised (open trades) | 🔴 -0.0569 |
| Started with | $20.0000 |
| Finished trades | 1 |
| Open now | 3 |
| Win rate | 0% (0/1) |

![balance](chart-equity.svg)

## Open right now

| Coin | Direction | Entry | Price now | Moved | P&L | on margin | Room to stop |
|---|---|---|---|---|---|---|---|
| **FIL** | SHORT 🔻 | 0.6813 | 0.6849 | +0.53% | 🔴 -0.0375 | -5.3% | 2.18% |
| **SAND** | SHORT 🔻 | 0.03898 | 0.03904 | +0.15% | 🔴 -0.0108 | -1.5% | 2.56% |
| **AXS** | SHORT 🔻 | 0.895 | 0.896 | +0.11% | 🔴 -0.0086 | -1.1% | 2.37% |
| | | | | **total** | **-0.0569** | | |

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
| ANKR | LONG | 0.73% | needs 0.7% move; volume below average |
| SNX | SHORT | 1.14% | needs 1.1% move; volume below average |
| EGLD | LONG | 1.67% | needs 1.7% move; volume below average |
| ICP | LONG | 1.80% | needs 1.8% move; volume below average |
| ENJ | SHORT | 1.83% | needs 1.8% move; volume below average |
| LRC | SHORT | 1.97% | needs 2.0% move; volume below average |
| STORJ | SHORT | 1.97% | needs 2.0% move; volume below average |
| AXS | SHORT | 2.06% | needs 2.1% move; volume below average |
| RVN | SHORT | 2.09% | needs 2.1% move; trend too weak (ADX 13/20) |
| SAND | SHORT | 2.23% | needs 2.2% move; volume below average |

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
