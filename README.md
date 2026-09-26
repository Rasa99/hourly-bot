# Hourly Trading Bot

**Updated 2026-09-26 00:07 UTC** &nbsp;·&nbsp; refreshes itself every hour

Paper money. $20 simulated, real Gate.io prices, no API keys — it cannot place a real order.

## Money

| | |
|---|---|
| **Equity now** | **$20.5492** 🟢 +2.75% |
| Settled balance | $20.4136 (+2.07%) |
| Unrealised (open trades) | 🟢 +0.1355 |
| Started with | $20.0000 |
| Finished trades | 52 |
| Open now | 1 |
| Win rate | 37% (19/52) |

![balance](chart-equity.svg)

## Open right now

| Coin | Direction | Entry | Price now | Moved | P&L | on margin | Room to stop |
|---|---|---|---|---|---|---|---|
| **MANA** | LONG 🔺 | 0.09099 | 0.09281 | +2.00% | 🟢 +0.1355 | +18.7% | 4.68% |
| | | | | **total** | **+0.1355** | | |

> ⚠️ **All 1 positions are long.** That is one bet on the same market direction, placed 1 times — these coins move together, so they will win together and lose together. Gross exposure is **36% of equity**.

![MANA](pos-MANA.png)


## What it is waiting for

**1 coin(s) ready to fire right now.** Scanned 47 coins.

![closest to entry](chart-closest.svg)

![what is blocking entries](chart-blockers.svg)

| Coin | Would be | Needs | Status |
|---|---|---|---|
| MANA | LONG | 0.00% | volume below average |
| QTUM | LONG | 0.00% | **READY** |
| THETA | LONG | 0.08% | needs 0.1% move; volume below average |
| IOTA | LONG | 0.20% | needs 0.2% move; volume below average |
| KSM | LONG | 0.23% | needs 0.2% move |
| GALA | LONG | 0.60% | needs 0.6% move |
| SOL | LONG | 0.66% | needs 0.7% move; volume below average |
| ONT | LONG | 0.69% | needs 0.7% move; volume below average |
| COMP | LONG | 0.70% | needs 0.7% move |
| SKL | LONG | 0.87% | needs 0.9% move; volume below average |

A trade needs **all four** of: price breaking its 3-day range, the trend filter agreeing, enough momentum (ADX over 20), and above-average volume. A coin at 0.00% that still has not traded is being held back by one of the other three — the table says which.

![market backdrop](chart-mood.svg)

## Results

![wins vs losses](chart-winloss.svg)

### Last 15 finished trades

| Coin | Direction | Result | Why it closed | When |
|---|---|---|---|---|
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
| FIL | LONG | 🟢 +0.3452 (+56.0%) | force_exit | 2026-09-19 09:28 |
| AVAX | LONG | 🟢 +0.8187 (+99.7%) | force_exit | 2026-09-19 09:28 |
| BAND | SHORT | 🔴 -0.2433 (-17.3%) | stop_loss | 2026-09-16 21:01 |

---

### How it works

Watches 47 coins every hour. Goes long when one breaks above its 3-day high, short when one breaks below its 3-day low — but only if the trend, momentum and volume all agree.

Every trade gets a stop-loss. Winners are left to run on a trailing stop rather than closed at a fixed target. It risks 1% of the account per trade and never holds more than 5 positions on the same side, so one bad day cannot end it.

**It loses more trades than it wins** — about 2-3 winners in 10, by design, with the winners much larger. Backtested on 2024-2026 it lost money. This is running on live prices with fake money to see what it actually does.
