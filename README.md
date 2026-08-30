# Hourly Trading Bot

**Updated 2026-08-30 03:07 UTC** &nbsp;·&nbsp; refreshes itself every hour

Paper money. $20 simulated, real Gate.io prices, no API keys — it cannot place a real order.

## Money

| | |
|---|---|
| **Equity now** | **$19.5363** 🔴 -2.32% |
| Settled balance | $19.4600 (-2.70%) |
| Unrealised (open trades) | 🟢 +0.0762 |
| Started with | $20.0000 |
| Finished trades | 3 |
| Open now | 6 |
| Win rate | 0% (0/3) |

![balance](chart-equity.svg)

## Open right now

| Coin | Direction | Entry | Price now | Moved | P&L | on margin | Room to stop |
|---|---|---|---|---|---|---|---|
| **FIL** | SHORT 🔻 | 0.6813 | 0.6765 | -0.70% | 🟢 +0.0433 | +6.1% | 3.44% |
| **SAND** | SHORT 🔻 | 0.03898 | 0.03836 | -1.59% | 🟢 +0.0673 | +9.6% | 4.38% |
| **AXS** | SHORT 🔻 | 0.895 | 0.8989 | +0.44% | 🔴 -0.0382 | -5.0% | 2.04% |
| **EGLD** | LONG 🔺 | 3.622 | 3.678 | +1.55% | 🟢 +0.1196 | +14.4% | 3.72% |
| **CRV** | SHORT 🔻 | 0.2973 | 0.3 | +0.91% | 🔴 -0.0959 | -9.5% | 0.97% |
| **UNI** | LONG 🔺 | 4.879 | 4.864 | -0.31% | 🔴 -0.0199 | -4.1% | 2.53% |
| | | | | **total** | **+0.0762** | | |

> 2 long / 4 short · gross exposure **232% of equity**.

![FIL](pos-FIL.png)

![SAND](pos-SAND.png)

![AXS](pos-AXS.png)

![EGLD](pos-EGLD.png)

![CRV](pos-CRV.png)

![UNI](pos-UNI.png)


## What it is waiting for

**2 coin(s) ready to fire right now.** Scanned 47 coins.

![closest to entry](chart-closest.svg)

![what is blocking entries](chart-blockers.svg)

| Coin | Would be | Needs | Status |
|---|---|---|---|
| UNI | LONG | 0.00% | **READY** |
| EGLD | LONG | 0.00% | **READY** |
| SNX | SHORT | 0.38% | needs 0.4% move |
| DOT | SHORT | 0.72% | needs 0.7% move; volume below average |
| ADA | SHORT | 0.90% | needs 0.9% move; volume below average |
| BCH | SHORT | 1.20% | needs 1.2% move; volume below average |
| FIL | SHORT | 1.51% | needs 1.5% move; volume below average |
| SAND | SHORT | 1.59% | needs 1.6% move; volume below average |
| LRC | SHORT | 1.85% | needs 1.9% move; volume below average |
| SKL | SHORT | 1.89% | needs 1.9% move; volume below average |

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
