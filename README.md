# Hourly Trading Bot

**Updated 2026-09-10 12:07 UTC** &nbsp;·&nbsp; refreshes itself every hour

Paper money. $20 simulated, real Gate.io prices, no API keys — it cannot place a real order.

## Money

| | |
|---|---|
| **Equity now** | **$21.6930** 🟢 +8.47% |
| Settled balance | $21.7910 (+8.95%) |
| Unrealised (open trades) | 🔴 -0.0979 |
| Started with | $20.0000 |
| Finished trades | 26 |
| Open now | 3 |
| Win rate | 46% (12/26) |

![balance](chart-equity.svg)

## Open right now

| Coin | Direction | Entry | Price now | Moved | P&L | on margin | Room to stop |
|---|---|---|---|---|---|---|---|
| **CRV** | SHORT 🔻 | 0.3377 | 0.339 | +0.38% | 🔴 -0.0302 | -4.8% | 2.92% |
| **MANA** | SHORT 🔻 | 0.07142 | 0.07175 | +0.46% | 🔴 -0.0568 | -5.6% | 1.60% |
| **BCH** | SHORT 🔻 | 245.11 | 245.23 | +0.05% | 🔴 -0.0110 | -1.5% | 2.14% |
| | | | | **total** | **-0.0979** | | |

> ⚠️ **All 3 positions are short.** That is one bet on the same market direction, placed 3 times — these coins move together, so they will win together and lose together. Gross exposure is **109% of equity**.

![CRV](pos-CRV.png)

![MANA](pos-MANA.png)

![BCH](pos-BCH.png)


## What it is waiting for

**0 coin(s) ready to fire right now.** Scanned 47 coins.

![closest to entry](chart-closest.svg)

![what is blocking entries](chart-blockers.svg)

| Coin | Would be | Needs | Status |
|---|---|---|---|
| AAVE | SHORT | 0.00% | volume below average |
| BCH | SHORT | 0.20% | needs 0.2% move; volume below average |
| BTC | SHORT | 0.27% | needs 0.3% move |
| MANA | SHORT | 0.53% | needs 0.5% move |
| HBAR | SHORT | 0.64% | needs 0.6% move; volume below average |
| SAND | SHORT | 0.67% | needs 0.7% move; RSI already stretched (20/22) |
| SOL | SHORT | 0.74% | needs 0.7% move |
| CELO | SHORT | 0.82% | needs 0.8% move; volume below average |
| APE | SHORT | 0.90% | needs 0.9% move; volume below average |
| AXS | SHORT | 0.91% | needs 0.9% move |

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
