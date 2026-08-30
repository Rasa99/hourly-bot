# Hourly Trading Bot

**Updated 2026-08-30 10:07 UTC** &nbsp;·&nbsp; refreshes itself every hour

Paper money. $20 simulated, real Gate.io prices, no API keys — it cannot place a real order.

## Money

| | |
|---|---|
| **Equity now** | **$19.4353** 🔴 -2.82% |
| Settled balance | $19.0456 (-4.77%) |
| Unrealised (open trades) | 🟢 +0.3897 |
| Started with | $20.0000 |
| Finished trades | 5 |
| Open now | 7 |
| Win rate | 0% (0/5) |

![balance](chart-equity.svg)

## Open right now

| Coin | Direction | Entry | Price now | Moved | P&L | on margin | Room to stop |
|---|---|---|---|---|---|---|---|
| **FIL** | SHORT 🔻 | 0.6813 | 0.6808 | -0.07% | 🔴 -0.0008 | -0.1% | 2.79% |
| **SAND** | SHORT 🔻 | 0.03898 | 0.03878 | -0.51% | 🔴 -0.0120 | -1.7% | 3.25% |
| **AXS** | SHORT 🔻 | 0.895 | 0.9055 | +1.17% | 🔴 -0.0942 | -12.2% | 1.29% |
| **EGLD** | LONG 🔺 | 3.622 | 3.95 | +9.06% | 🟢 +0.7440 | +89.3% | 6.13% |
| **CRV** | SHORT 🔻 | 0.2973 | 0.2983 | +0.34% | 🔴 -0.0389 | -3.8% | 1.54% |
| **UNI** | LONG 🔺 | 4.879 | 4.82 | -1.21% | 🔴 -0.0641 | -13.1% | 1.64% |
| **KSM** | LONG 🔺 | 3.636 | 3.593 | -1.18% | 🔴 -0.1443 | -12.8% | 0.45% |
| | | | | **total** | **+0.3897** | | |

> 3 long / 4 short · gross exposure **296% of equity**.

![FIL](pos-FIL.png)

![SAND](pos-SAND.png)

![AXS](pos-AXS.png)

![EGLD](pos-EGLD.png)

![CRV](pos-CRV.png)

![UNI](pos-UNI.png)

![KSM](pos-KSM.png)


## What it is waiting for

**1 coin(s) ready to fire right now.** Scanned 47 coins.

![closest to entry](chart-closest.svg)

![what is blocking entries](chart-blockers.svg)

| Coin | Would be | Needs | Status |
|---|---|---|---|
| EGLD | LONG | 0.00% | **READY** |
| CRV | SHORT | 0.60% | needs 0.6% move; volume below average |
| ADA | SHORT | 0.85% | needs 0.8% move; trend too weak (ADX 17/20) |
| RVN | SHORT | 0.94% | needs 0.9% move; trend too weak (ADX 15/20) |
| BCH | SHORT | 1.06% | needs 1.1% move; volume below average |
| KSM | LONG | 1.14% | needs 1.1% move; volume below average |
| ALGO | SHORT | 1.18% | needs 1.2% move; volume below average |
| DOT | SHORT | 1.54% | needs 1.5% move; trend too weak (ADX 19/20) |
| HBAR | SHORT | 1.55% | needs 1.5% move; trend too weak (ADX 19/20) |
| ATOM | SHORT | 1.56% | needs 1.6% move; trend too weak (ADX 13/20) |

A trade needs **all four** of: price breaking its 3-day range, the trend filter agreeing, enough momentum (ADX over 20), and above-average volume. A coin at 0.00% that still has not traded is being held back by one of the other three — the table says which.

![market backdrop](chart-mood.svg)

## Results

![wins vs losses](chart-winloss.svg)

### Last 15 finished trades

| Coin | Direction | Result | Why it closed | When |
|---|---|---|---|---|
| THETA | SHORT | 🔴 -0.2014 (-14.1%) | stop_loss | 2026-08-30 06:59 |
| MANA | LONG | 🔴 -0.2131 (-17.8%) | stop_loss | 2026-08-30 04:42 |
| ICP | LONG | 🔴 -0.2062 (-24.6%) | stop_loss | 2026-08-30 01:13 |
| BCH | SHORT | 🔴 -0.1922 (-19.8%) | trailing_stop_loss | 2026-08-29 20:06 |
| UNI | LONG | 🔴 -0.1416 (-30.3%) | trailing_stop_loss | 2026-08-28 10:07 |

---

### How it works

Watches 47 coins every hour. Goes long when one breaks above its 3-day high, short when one breaks below its 3-day low — but only if the trend, momentum and volume all agree.

Every trade gets a stop-loss. Winners are left to run on a trailing stop rather than closed at a fixed target. It risks 1% of the account per trade and never holds more than 5 positions on the same side, so one bad day cannot end it.

**It loses more trades than it wins** — about 2-3 winners in 10, by design, with the winners much larger. Backtested on 2024-2026 it lost money. This is running on live prices with fake money to see what it actually does.
