# Hourly Trading Bot

**Updated 2026-09-27 23:07 UTC** &nbsp;·&nbsp; refreshes itself every hour

Paper money. $20 simulated, real Gate.io prices, no API keys — it cannot place a real order.

## Money

| | |
|---|---|
| **Equity now** | **$19.7041** 🔴 -1.48% |
| Settled balance | $19.8194 (-0.90%) |
| Unrealised (open trades) | 🔴 -0.1153 |
| Started with | $20.0000 |
| Finished trades | 55 |
| Open now | 2 |
| Win rate | 35% (19/55) |

![balance](chart-equity.svg)

## Open right now

| Coin | Direction | Entry | Price now | Moved | P&L | on margin | Room to stop |
|---|---|---|---|---|---|---|---|
| **MANA** | LONG 🔺 | 0.09099 | 0.0916 | +0.67% | 🟢 +0.0355 | +4.9% | 3.42% |
| **NEAR** | LONG 🔺 | 5.5518 | 5.4065 | -2.62% | 🔴 -0.1508 | -27.2% | 1.77% |
| | | | | **total** | **-0.1153** | | |

> ⚠️ **All 2 positions are long.** That is one bet on the same market direction, placed 2 times — these coins move together, so they will win together and lose together. Gross exposure is **65% of equity**.

![MANA](pos-MANA.png)

![NEAR](pos-NEAR.png)


## What it is waiting for

**0 coin(s) ready to fire right now.** Scanned 47 coins.

![closest to entry](chart-closest.svg)

![what is blocking entries](chart-blockers.svg)

| Coin | Would be | Needs | Status |
|---|---|---|---|
| STORJ | SHORT | 0.98% | needs 1.0% move; trend too weak (ADX 12/20) |
| BTC | LONG | 1.25% | needs 1.3% move; trend too weak (ADX 13/20) |
| BNB | LONG | 1.39% | needs 1.4% move; trend too weak (ADX 12/20) |
| SNX | LONG | 1.60% | needs 1.6% move |
| ETC | LONG | 2.05% | needs 2.1% move; trend too weak (ADX 10/20) |
| BAT | LONG | 2.10% | needs 2.1% move; volume below average |
| MANA | LONG | 2.14% | needs 2.1% move; trend too weak (ADX 14/20) |
| AAVE | LONG | 2.14% | needs 2.1% move; trend too weak (ADX 15/20) |
| SKL | LONG | 2.36% | needs 2.4% move; trend too weak (ADX 13/20) |
| NEAR | LONG | 2.42% | needs 2.4% move |

A trade needs **all four** of: price breaking its 3-day range, the trend filter agreeing, enough momentum (ADX over 20), and above-average volume. A coin at 0.00% that still has not traded is being held back by one of the other three — the table says which.

![market backdrop](chart-mood.svg)

## Results

![wins vs losses](chart-winloss.svg)

### Last 15 finished trades

| Coin | Direction | Result | Why it closed | When |
|---|---|---|---|---|
| SAND | LONG | 🔴 -0.2134 (-27.8%) | stop_loss | 2026-09-26 20:04 |
| ICP | LONG | 🔴 -0.2077 (-32.8%) | stop_loss | 2026-09-26 18:45 |
| DOT | LONG | 🔴 -0.1731 (-33.7%) | stop_loss | 2026-09-26 19:19 |
| ALGO | LONG | 🔴 -0.1848 (-31.4%) | trailing_stop_loss | 2026-09-25 14:03 |
| NEAR | LONG | 🟢 +0.1803 (+29.6%) | force_exit | 2026-09-25 15:27 |
| LINK | LONG | 🟢 +0.4337 (+32.3%) | force_exit | 2026-09-25 15:27 |
| LTC | LONG | 🔴 -0.3727 (-51.2%) | stop_loss | 2026-09-25 13:47 |
| NEAR | LONG | 🔴 -0.2758 (-51.5%) | stop_loss | 2026-09-23 14:13 |
| HBAR | LONG | 🔴 -0.1833 (-37.7%) | stop_loss | 2026-09-22 10:24 |
| GRT | LONG | 🟢 +0.1471 (+23.7%) | force_exit | 2026-09-21 03:14 |
| ALGO | LONG | 🔴 -0.1920 (-42.4%) | stop_loss | 2026-09-20 21:11 |
| HBAR | LONG | 🔴 -0.2020 (-32.9%) | stop_loss | 2026-09-20 19:21 |
| DASH | LONG | 🔴 -0.1733 (-45.7%) | stop_loss | 2026-09-19 05:58 |
| CELO | LONG | 🟢 +0.1347 (+11.6%) | force_exit | 2026-09-19 09:28 |
| ADA | LONG | 🔴 -0.0111 (-1.6%) | force_exit | 2026-09-19 09:28 |

---

### How it works

Watches 47 coins every hour. Goes long when one breaks above its 3-day high, short when one breaks below its 3-day low — but only if the trend, momentum and volume all agree.

Every trade gets a stop-loss. Winners are left to run on a trailing stop rather than closed at a fixed target. It risks 1% of the account per trade and never holds more than 5 positions on the same side, so one bad day cannot end it.

**It loses more trades than it wins** — about 2-3 winners in 10, by design, with the winners much larger. Backtested on 2024-2026 it lost money. This is running on live prices with fake money to see what it actually does.
