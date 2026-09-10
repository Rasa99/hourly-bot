# Hourly Trading Bot

**Updated 2026-09-10 10:07 UTC** &nbsp;·&nbsp; refreshes itself every hour

Paper money. $20 simulated, real Gate.io prices, no API keys — it cannot place a real order.

## Money

| | |
|---|---|
| **Equity now** | **$21.9473** 🟢 +9.74% |
| Settled balance | $21.8139 (+9.07%) |
| Unrealised (open trades) | 🟢 +0.1334 |
| Started with | $20.0000 |
| Finished trades | 24 |
| Open now | 4 |
| Win rate | 46% (11/24) |

![balance](chart-equity.svg)

## Open right now

| Coin | Direction | Entry | Price now | Moved | P&L | on margin | Room to stop |
|---|---|---|---|---|---|---|---|
| **AAVE** | SHORT 🔻 | 125.97 | 123.9 | -1.64% | 🟢 +0.1375 | +15.6% | 4.03% |
| **CRV** | SHORT 🔻 | 0.3377 | 0.3391 | +0.41% | 🔴 -0.0321 | -5.0% | 2.89% |
| **EGLD** | LONG 🔺 | 5.305 | 5.347 | +0.79% | 🟢 +0.0367 | +6.9% | 4.79% |
| **MANA** | SHORT 🔻 | 0.07142 | 0.07141 | -0.01% | 🔴 -0.0087 | -0.9% | 2.09% |
| | | | | **total** | **+0.1334** | | |

> 1 long / 3 short · gross exposure **140% of equity**.

![AAVE](pos-AAVE.png)

![CRV](pos-CRV.png)

![EGLD](pos-EGLD.png)

![MANA](pos-MANA.png)


## What it is waiting for

**0 coin(s) ready to fire right now.** Scanned 47 coins.

![closest to entry](chart-closest.svg)

![what is blocking entries](chart-blockers.svg)

| Coin | Would be | Needs | Status |
|---|---|---|---|
| MANA | SHORT | 0.00% | volume below average |
| RVN | SHORT | 0.00% | RSI already stretched (17/22) |
| BCH | SHORT | 0.17% | needs 0.2% move; volume below average |
| AAVE | SHORT | 0.24% | needs 0.2% move; volume below average |
| SAND | SHORT | 0.25% | needs 0.3% move; volume below average |
| HBAR | SHORT | 0.36% | needs 0.4% move; volume below average |
| BTC | SHORT | 0.47% | needs 0.5% move; volume below average |
| GALA | SHORT | 0.75% | needs 0.8% move; volume below average |
| SNX | SHORT | 0.76% | needs 0.8% move; volume below average |
| SOL | SHORT | 0.87% | needs 0.9% move; volume below average |

A trade needs **all four** of: price breaking its 3-day range, the trend filter agreeing, enough momentum (ADX over 20), and above-average volume. A coin at 0.00% that still has not traded is being held back by one of the other three — the table says which.

![market backdrop](chart-mood.svg)

## Results

![wins vs losses](chart-winloss.svg)

### Last 15 finished trades

| Coin | Direction | Result | Why it closed | When |
|---|---|---|---|---|
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
| MANA | LONG | 🔴 -0.2131 (-17.8%) | stop_loss | 2026-08-30 04:42 |

---

### How it works

Watches 47 coins every hour. Goes long when one breaks above its 3-day high, short when one breaks below its 3-day low — but only if the trend, momentum and volume all agree.

Every trade gets a stop-loss. Winners are left to run on a trailing stop rather than closed at a fixed target. It risks 1% of the account per trade and never holds more than 5 positions on the same side, so one bad day cannot end it.

**It loses more trades than it wins** — about 2-3 winners in 10, by design, with the winners much larger. Backtested on 2024-2026 it lost money. This is running on live prices with fake money to see what it actually does.
