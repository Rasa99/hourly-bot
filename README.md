# Hourly Trading Bot

**Updated 2026-09-10 13:07 UTC** &nbsp;·&nbsp; refreshes itself every hour

Paper money. $20 simulated, real Gate.io prices, no API keys — it cannot place a real order.

## Money

| | |
|---|---|
| **Equity now** | **$21.9366** 🟢 +9.68% |
| Settled balance | $21.7910 (+8.95%) |
| Unrealised (open trades) | 🟢 +0.1456 |
| Started with | $20.0000 |
| Finished trades | 26 |
| Open now | 3 |
| Win rate | 46% (12/26) |

![balance](chart-equity.svg)

## Open right now

| Coin | Direction | Entry | Price now | Moved | P&L | on margin | Room to stop |
|---|---|---|---|---|---|---|---|
| **CRV** | SHORT 🔻 | 0.3377 | 0.3394 | +0.50% | 🔴 -0.0377 | -5.9% | 2.80% |
| **MANA** | SHORT 🔻 | 0.07142 | 0.07138 | -0.06% | 🔴 -0.0044 | -0.4% | 2.13% |
| **BCH** | SHORT 🔻 | 245.11 | 238.61 | -2.65% | 🟢 +0.1877 | +25.5% | 4.97% |
| | | | | **total** | **+0.1456** | | |

> ⚠️ **All 3 positions are short.** That is one bet on the same market direction, placed 3 times — these coins move together, so they will win together and lose together. Gross exposure is **109% of equity**.

![CRV](pos-CRV.png)

![MANA](pos-MANA.png)

![BCH](pos-BCH.png)


## What it is waiting for

**12 coin(s) ready to fire right now.** Scanned 47 coins.

![closest to entry](chart-closest.svg)

![what is blocking entries](chart-blockers.svg)

| Coin | Would be | Needs | Status |
|---|---|---|---|
| BTC | SHORT | 0.00% | **READY** |
| SOL | SHORT | 0.00% | **READY** |
| DOGE | SHORT | 0.00% | **READY** |
| BCH | SHORT | 0.00% | RSI already stretched (21/22) |
| HBAR | SHORT | 0.00% | **READY** |
| APE | SHORT | 0.00% | **READY** |
| SAND | SHORT | 0.00% | RSI already stretched (15/22) |
| MANA | SHORT | 0.00% | **READY** |
| AXS | SHORT | 0.00% | **READY** |
| THETA | SHORT | 0.00% | **READY** |

A trade needs **all four** of: price breaking its 3-day range, the trend filter agreeing, enough momentum (ADX over 20), and above-average volume. A coin at 0.00% that still has not traded is being held back by one of the other three — the table says which.

![market backdrop](chart-mood.svg)

## Results

![wins vs losses](chart-winloss.svg)

### Last 15 finished trades

| Coin | Direction | Result | Why it closed | When |
|---|---|---|---|---|
| EGLD | LONG | 🔴 -0.2262 (-42.6%) | stop_loss | 2026-09-10 11:05 |
| AAVE | SHORT | 🟢 +0.2033 (+23.1%) | force_exit | 2026-09-10 11:07 |
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

---

### How it works

Watches 47 coins every hour. Goes long when one breaks above its 3-day high, short when one breaks below its 3-day low — but only if the trend, momentum and volume all agree.

Every trade gets a stop-loss. Winners are left to run on a trailing stop rather than closed at a fixed target. It risks 1% of the account per trade and never holds more than 5 positions on the same side, so one bad day cannot end it.

**It loses more trades than it wins** — about 2-3 winners in 10, by design, with the winners much larger. Backtested on 2024-2026 it lost money. This is running on live prices with fake money to see what it actually does.
