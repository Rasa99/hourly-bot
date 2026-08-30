# Hourly Trading Bot

**Updated 2026-08-30 07:07 UTC** &nbsp;·&nbsp; refreshes itself every hour

Paper money. $20 simulated, real Gate.io prices, no API keys — it cannot place a real order.

## Money

| | |
|---|---|
| **Equity now** | **$19.2362** 🔴 -3.82% |
| Settled balance | $19.0456 (-4.77%) |
| Unrealised (open trades) | 🟢 +0.1906 |
| Started with | $20.0000 |
| Finished trades | 5 |
| Open now | 7 |
| Win rate | 0% (0/5) |

![balance](chart-equity.svg)

## Open right now

| Coin | Direction | Entry | Price now | Moved | P&L | on margin | Room to stop |
|---|---|---|---|---|---|---|---|
| **FIL** | SHORT 🔻 | 0.6813 | 0.6816 | +0.04% | 🔴 -0.0098 | -1.4% | 2.67% |
| **SAND** | SHORT 🔻 | 0.03898 | 0.03855 | -1.10% | 🟢 +0.0330 | +4.7% | 3.87% |
| **AXS** | SHORT 🔻 | 0.895 | 0.9076 | +1.41% | 🔴 -0.1130 | -14.7% | 1.06% |
| **EGLD** | LONG 🔺 | 3.622 | 3.795 | +4.78% | 🟢 +0.3885 | +46.6% | 5.51% |
| **CRV** | SHORT 🔻 | 0.2973 | 0.3003 | +1.01% | 🔴 -0.1061 | -10.5% | 0.87% |
| **UNI** | LONG 🔺 | 4.879 | 4.952 | +1.50% | 🟢 +0.0681 | +14.0% | 4.26% |
| **KSM** | LONG 🔺 | 3.636 | 3.617 | -0.52% | 🔴 -0.0701 | -6.2% | 1.11% |
| | | | | **total** | **+0.1906** | | |

> 3 long / 4 short · gross exposure **296% of equity**.

![FIL](pos-FIL.png)

![SAND](pos-SAND.png)

![AXS](pos-AXS.png)

![EGLD](pos-EGLD.png)

![CRV](pos-CRV.png)

![UNI](pos-UNI.png)

![KSM](pos-KSM.png)


## What it is waiting for

**2 coin(s) ready to fire right now.** Scanned 47 coins.

![closest to entry](chart-closest.svg)

![what is blocking entries](chart-blockers.svg)

| Coin | Would be | Needs | Status |
|---|---|---|---|
| UNI | LONG | 0.00% | **READY** |
| EGLD | LONG | 0.00% | **READY** |
| KSM | LONG | 0.66% | needs 0.7% move; volume below average |
| THETA | SHORT | 1.18% | needs 1.2% move; volume below average |
| BCH | SHORT | 1.36% | needs 1.4% move; volume below average |
| CRV | SHORT | 1.36% | needs 1.4% move; volume below average |
| MANA | LONG | 1.48% | needs 1.5% move |
| STORJ | SHORT | 1.62% | needs 1.6% move; volume below average |
| DOT | SHORT | 1.66% | needs 1.7% move |
| ADA | SHORT | 1.73% | needs 1.7% move; trend too weak (ADX 19/20) |

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
