# Hourly Trading Bot

**Updated 2026-09-30 16:07 UTC** &nbsp;·&nbsp; refreshes itself every hour

Paper money. $20 simulated, real Gate.io prices, no API keys — it cannot place a real order.

## Money

| | |
|---|---|
| **Equity now** | **$19.0452** 🔴 -4.77% |
| Settled balance | $18.9958 (-5.02%) |
| Unrealised (open trades) | 🟢 +0.0494 |
| Started with | $20.0000 |
| Finished trades | 59 |
| Open now | 1 |
| Win rate | 32% (19/59) |

![balance](chart-equity.svg)

## Open right now

| Coin | Direction | Entry | Price now | Moved | P&L | on margin | Room to stop |
|---|---|---|---|---|---|---|---|
| **CRV** | LONG 🔺 | 0.3856 | 0.3908 | +1.35% | 🟢 +0.0494 | +12.0% | 5.89% |
| | | | | **total** | **+0.0494** | | |

> ⚠️ **All 1 positions are long.** That is one bet on the same market direction, placed 1 times — these coins move together, so they will win together and lose together. Gross exposure is **22% of equity**.

![CRV](pos-CRV.png)


## What it is waiting for

**0 coin(s) ready to fire right now.** Scanned 47 coins.

![closest to entry](chart-closest.svg)

![what is blocking entries](chart-blockers.svg)

| Coin | Would be | Needs | Status |
|---|---|---|---|
| SUSHI | LONG | 0.33% | needs 0.3% move |
| BCH | SHORT | 1.63% | needs 1.6% move |
| BTC | LONG | 1.82% | needs 1.8% move |
| QTUM | LONG | 2.01% | needs 2.0% move; volume below average |
| CHZ | LONG | 2.32% | needs 2.3% move; volume below average |
| AXS | LONG | 2.37% | needs 2.4% move; trend too weak (ADX 18/20) |
| ETH | LONG | 2.47% | needs 2.5% move; trend too weak (ADX 17/20) |
| BNB | SHORT | 2.50% | needs 2.5% move; trend too weak (ADX 19/20) |
| ONT | LONG | 2.70% | needs 2.7% move; trend too weak (ADX 20/20) |
| ICP | LONG | 2.78% | needs 2.8% move; volume below average |

A trade needs **all four** of: price breaking its 3-day range, the trend filter agreeing, enough momentum (ADX over 20), and above-average volume. A coin at 0.00% that still has not traded is being held back by one of the other three — the table says which.

![market backdrop](chart-mood.svg)

## Results

![wins vs losses](chart-winloss.svg)

### Last 15 finished trades

| Coin | Direction | Result | Why it closed | When |
|---|---|---|---|---|
| SKL | LONG | 🔴 -0.1959 (-25.9%) | stop_loss | 2026-09-30 13:36 |
| ALGO | LONG | 🔴 -0.1663 (-51.0%) | stop_loss | 2026-09-29 07:08 |
| NEAR | LONG | 🔴 -0.2461 (-44.3%) | stop_loss | 2026-09-28 00:36 |
| SAND | LONG | 🔴 -0.2134 (-27.8%) | stop_loss | 2026-09-26 20:04 |
| ICP | LONG | 🔴 -0.2077 (-32.8%) | stop_loss | 2026-09-26 18:45 |
| DOT | LONG | 🔴 -0.1731 (-33.7%) | stop_loss | 2026-09-26 19:19 |
| ALGO | LONG | 🔴 -0.1848 (-31.4%) | trailing_stop_loss | 2026-09-25 14:03 |
| NEAR | LONG | 🟢 +0.1803 (+29.6%) | force_exit | 2026-09-25 15:27 |
| MANA | LONG | 🔴 -0.2154 (-29.7%) | stop_loss | 2026-09-28 03:33 |
| LINK | LONG | 🟢 +0.4337 (+32.3%) | force_exit | 2026-09-25 15:27 |
| LTC | LONG | 🔴 -0.3727 (-51.2%) | stop_loss | 2026-09-25 13:47 |
| NEAR | LONG | 🔴 -0.2758 (-51.5%) | stop_loss | 2026-09-23 14:13 |
| HBAR | LONG | 🔴 -0.1833 (-37.7%) | stop_loss | 2026-09-22 10:24 |
| GRT | LONG | 🟢 +0.1471 (+23.7%) | force_exit | 2026-09-21 03:14 |
| ALGO | LONG | 🔴 -0.1920 (-42.4%) | stop_loss | 2026-09-20 21:11 |

---

### How it works

Watches 47 coins every hour. Goes long when one breaks above its 3-day high, short when one breaks below its 3-day low — but only if the trend, momentum and volume all agree.

Every trade gets a stop-loss. Winners are left to run on a trailing stop rather than closed at a fixed target. It risks 1% of the account per trade and never holds more than 5 positions on the same side, so one bad day cannot end it.

**It loses more trades than it wins** — about 2-3 winners in 10, by design, with the winners much larger. Backtested on 2024-2026 it lost money. This is running on live prices with fake money to see what it actually does.
