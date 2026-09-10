# Hourly Trading Bot

**Updated 2026-09-10 11:07 UTC** &nbsp;·&nbsp; refreshes itself every hour

Paper money. $20 simulated, real Gate.io prices, no API keys — it cannot place a real order.

## Money

| | |
|---|---|
| **Equity now** | **$21.7809** 🟢 +8.90% |
| Settled balance | $21.5877 (+7.94%) |
| Unrealised (open trades) | 🟢 +0.1932 |
| Started with | $20.0000 |
| Finished trades | 25 |
| Open now | 4 |
| Win rate | 44% (11/25) |

![balance](chart-equity.svg)

## Open right now

| Coin | Direction | Entry | Price now | Moved | P&L | on margin | Room to stop |
|---|---|---|---|---|---|---|---|
| **AAVE** | SHORT 🔻 | 125.97 | 122.87 | -2.46% | 🟢 +0.2096 | +23.8% | 4.90% |
| **CRV** | SHORT 🔻 | 0.3377 | 0.3387 | +0.30% | 🔴 -0.0245 | -3.9% | 3.01% |
| **MANA** | SHORT 🔻 | 0.07142 | 0.07122 | -0.28% | 🟢 +0.0182 | +1.8% | 2.36% |
| **BCH** | SHORT 🔻 | 245.11 | 245.2 | +0.04% | 🔴 -0.0101 | -1.4% | 2.18% |
| | | | | **total** | **+0.1932** | | |

> ⚠️ **All 4 positions are short.** That is one bet on the same market direction, placed 4 times — these coins move together, so they will win together and lose together. Gross exposure is **151% of equity**.

![AAVE](pos-AAVE.png)

![CRV](pos-CRV.png)

![MANA](pos-MANA.png)

![BCH](pos-BCH.png)


## What it is waiting for

**2 coin(s) ready to fire right now.** Scanned 47 coins.

![closest to entry](chart-closest.svg)

![what is blocking entries](chart-blockers.svg)

| Coin | Would be | Needs | Status |
|---|---|---|---|
| BCH | SHORT | 0.00% | **READY** |
| AAVE | SHORT | 0.00% | **READY** |
| CELO | SHORT | 0.00% | volume below average |
| SAND | SHORT | 0.11% | needs 0.1% move; volume below average |
| BTC | SHORT | 0.30% | needs 0.3% move; volume below average |
| HBAR | SHORT | 0.36% | needs 0.4% move; volume below average |
| GALA | SHORT | 0.41% | needs 0.4% move; volume below average |
| MANA | SHORT | 0.61% | needs 0.6% move; volume below average |
| SOL | SHORT | 0.79% | needs 0.8% move; volume below average |
| CRV | SHORT | 0.80% | needs 0.8% move |

A trade needs **all four** of: price breaking its 3-day range, the trend filter agreeing, enough momentum (ADX over 20), and above-average volume. A coin at 0.00% that still has not traded is being held back by one of the other three — the table says which.

![market backdrop](chart-mood.svg)

## Results

![wins vs losses](chart-winloss.svg)

### Last 15 finished trades

| Coin | Direction | Result | Why it closed | When |
|---|---|---|---|---|
| EGLD | LONG | 🔴 -0.2262 (-42.6%) | stop_loss | 2026-09-10 11:05 |
| ALGO | LONG | 🟢 +0.1357 (+19.3%) | force_exit | 2026-09-08 16:07 |
| ATOM | LONG | 🟢 +0.4604 (+54.2%) | force_exit | 2026-09-08 16:07 |
| ETC | LONG | 🟢 +0.3342 (+50.9%) | force_exit | 2026-09-08 16:07 |
| DOT | LONG | 🟢 +0.4297 (+100.5%) | force_exit | 2026-09-08 16:07 |
| UNI | LONG | 🔴 -0.0737 (-10.9%) | force_exit | 2026-09-05 17:25 |
| SUSHI | LONG | 🟢 +0.8701 (+120.0%) | force_exit | 2026-09-05 17:24 |
| DOT | LONG | 🟢 +0.3555 (+55.3%) | force_exit | 2026-09-06 14:09 |
| LINK | LONG | 🔴 -0.2654 (-22.0%) | stop_loss | 2026-09-04 12:30 |
| DASH | LONG | 🟢 +0.3396 (+75.4%) | force_exit | 2026-09-04 09:07 |
| EGLD | LONG | 🟢 +0.7674 (+147.5%) | trailing_stop_loss | 2026-09-03 00:18 |
| LINK | SHORT | 🔴 -0.2467 (-22.5%) | stop_loss | 2026-09-02 13:45 |
| DASH | LONG | 🔴 -0.1861 (-35.0%) | stop_loss | 2026-08-30 20:43 |
| KSM | LONG | 🔴 -0.2021 (-17.9%) | stop_loss | 2026-08-30 20:40 |
| THETA | SHORT | 🔴 -0.2014 (-14.1%) | stop_loss | 2026-08-30 06:59 |

---

### How it works

Watches 47 coins every hour. Goes long when one breaks above its 3-day high, short when one breaks below its 3-day low — but only if the trend, momentum and volume all agree.

Every trade gets a stop-loss. Winners are left to run on a trailing stop rather than closed at a fixed target. It risks 1% of the account per trade and never holds more than 5 positions on the same side, so one bad day cannot end it.

**It loses more trades than it wins** — about 2-3 winners in 10, by design, with the winners much larger. Backtested on 2024-2026 it lost money. This is running on live prices with fake money to see what it actually does.
