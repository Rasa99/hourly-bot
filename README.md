# Hourly Trading Bot

**Updated 2026-08-30 19:07 UTC** &nbsp;·&nbsp; refreshes itself every hour

Paper money. $20 simulated, real Gate.io prices, no API keys — it cannot place a real order.

## Money

| | |
|---|---|
| **Equity now** | **$19.3790** 🔴 -3.10% |
| Settled balance | $19.0347 (-4.83%) |
| Unrealised (open trades) | 🟢 +0.3443 |
| Started with | $20.0000 |
| Finished trades | 8 |
| Open now | 5 |
| Win rate | 12% (1/8) |

![balance](chart-equity.svg)

## Open right now

| Coin | Direction | Entry | Price now | Moved | P&L | on margin | Room to stop |
|---|---|---|---|---|---|---|---|
| **FIL** | SHORT 🔻 | 0.6813 | 0.692 | +1.57% | 🔴 -0.1173 | -16.5% | 1.13% |
| **SAND** | SHORT 🔻 | 0.03898 | 0.03911 | +0.33% | 🔴 -0.0754 | -10.8% | 2.38% |
| **UNI** | LONG 🔺 | 4.879 | 5.43 | +11.29% | 🟢 +0.5453 | +111.8% | 6.85% |
| **KSM** | LONG 🔺 | 3.636 | 3.641 | +0.14% | 🟢 +0.0055 | +0.5% | 1.76% |
| **DASH** | LONG 🔺 | 44.22 | 44.15 | -0.16% | 🔴 -0.0137 | -2.6% | 3.24% |
| | | | | **total** | **+0.3443** | | |

> 3 long / 2 short · gross exposure **187% of equity**.

![FIL](pos-FIL.png)

![SAND](pos-SAND.png)

![UNI](pos-UNI.png)

![KSM](pos-KSM.png)

![DASH](pos-DASH.png)


## What it is waiting for

**1 coin(s) ready to fire right now.** Scanned 47 coins.

![closest to entry](chart-closest.svg)

![what is blocking entries](chart-blockers.svg)

| Coin | Would be | Needs | Status |
|---|---|---|---|
| DASH | LONG | 0.00% | **READY** |
| KSM | LONG | 0.19% | needs 0.2% move |
| UNI | LONG | 0.86% | needs 0.9% move; volume below average |
| ETH | LONG | 0.98% | needs 1.0% move |
| RVN | SHORT | 1.18% | needs 1.2% move; trend too weak (ADX 14/20) |
| STORJ | SHORT | 1.21% | needs 1.2% move; volume below average |
| ANKR | LONG | 1.98% | needs 2.0% move; trend too weak (ADX 10/20) |
| AVAX | LONG | 1.99% | needs 2.0% move; volume below average |
| SUSHI | LONG | 2.05% | needs 2.0% move; volume below average |
| ENJ | SHORT | 2.19% | needs 2.2% move; trend too weak (ADX 15/20) |

A trade needs **all four** of: price breaking its 3-day range, the trend filter agreeing, enough momentum (ADX over 20), and above-average volume. A coin at 0.00% that still has not traded is being held back by one of the other three — the table says which.

![market backdrop](chart-mood.svg)

## Results

![wins vs losses](chart-winloss.svg)

### Last 15 finished trades

| Coin | Direction | Result | Why it closed | When |
|---|---|---|---|---|
| THETA | SHORT | 🔴 -0.2014 (-14.1%) | stop_loss | 2026-08-30 06:59 |
| MANA | LONG | 🔴 -0.2131 (-17.8%) | stop_loss | 2026-08-30 04:42 |
| CRV | SHORT | 🔴 -0.1984 (-19.6%) | stop_loss | 2026-08-30 12:09 |
| EGLD | LONG | 🟢 +0.3823 (+45.9%) | trailing_stop_loss | 2026-08-30 17:24 |
| ICP | LONG | 🔴 -0.2062 (-24.6%) | stop_loss | 2026-08-30 01:13 |
| BCH | SHORT | 🔴 -0.1922 (-19.8%) | trailing_stop_loss | 2026-08-29 20:06 |
| AXS | SHORT | 🔴 -0.1948 (-25.3%) | trailing_stop_loss | 2026-08-30 12:07 |
| UNI | LONG | 🔴 -0.1416 (-30.3%) | trailing_stop_loss | 2026-08-28 10:07 |

---

### How it works

Watches 47 coins every hour. Goes long when one breaks above its 3-day high, short when one breaks below its 3-day low — but only if the trend, momentum and volume all agree.

Every trade gets a stop-loss. Winners are left to run on a trailing stop rather than closed at a fixed target. It risks 1% of the account per trade and never holds more than 5 positions on the same side, so one bad day cannot end it.

**It loses more trades than it wins** — about 2-3 winners in 10, by design, with the winners much larger. Backtested on 2024-2026 it lost money. This is running on live prices with fake money to see what it actually does.
