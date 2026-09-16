# Hourly Trading Bot

**Updated 2026-09-16 03:07 UTC** &nbsp;·&nbsp; refreshes itself every hour

Paper money. $20 simulated, real Gate.io prices, no API keys — it cannot place a real order.

## Money

| | |
|---|---|
| **Equity now** | **$21.7011** 🟢 +8.51% |
| Settled balance | $21.2203 (+6.10%) |
| Unrealised (open trades) | 🟢 +0.4807 |
| Started with | $20.0000 |
| Finished trades | 32 |
| Open now | 5 |
| Win rate | 41% (13/32) |

![balance](chart-equity.svg)

## Open right now

| Coin | Direction | Entry | Price now | Moved | P&L | on margin | Room to stop |
|---|---|---|---|---|---|---|---|
| **RVN** | SHORT 🔻 | 0.002126 | 0.002105 | -0.99% | 🟢 +0.0628 | +7.9% | 3.66% |
| **ICP** | SHORT 🔻 | 2.557 | 2.465 | -3.60% | 🟢 +0.2682 | +34.9% | 6.57% |
| **DOT** | SHORT 🔻 | 0.953 | 0.948 | -0.52% | 🟢 +0.0278 | +4.2% | 3.48% |
| **CRV** | SHORT 🔻 | 0.3239 | 0.3157 | -2.53% | 🟢 +0.1359 | +24.8% | 6.49% |
| **AAVE** | SHORT 🔻 | 120.91 | 121.08 | +0.14% | 🔴 -0.0139 | -2.3% | 2.84% |
| | | | | **total** | **+0.4807** | | |

> ⚠️ **All 5 positions are short.** That is one bet on the same market direction, placed 5 times — these coins move together, so they will win together and lose together. Gross exposure is **159% of equity**.

![RVN](pos-RVN.png)

![ICP](pos-ICP.png)

![DOT](pos-DOT.png)

![CRV](pos-CRV.png)

![AAVE](pos-AAVE.png)


## What it is waiting for

**0 coin(s) ready to fire right now.** Scanned 47 coins.

![closest to entry](chart-closest.svg)

![what is blocking entries](chart-blockers.svg)

| Coin | Would be | Needs | Status |
|---|---|---|---|
| BAND | SHORT | 0.00% | volume below average |
| ATOM | SHORT | 0.60% | needs 0.6% move; volume below average |
| AAVE | SHORT | 0.72% | needs 0.7% move |
| HBAR | SHORT | 0.75% | needs 0.8% move; volume below average |
| BNB | SHORT | 0.76% | needs 0.8% move; volume below average |
| ICP | SHORT | 0.77% | needs 0.8% move; volume below average |
| LINK | SHORT | 0.82% | needs 0.8% move; volume below average |
| LTC | SHORT | 0.86% | needs 0.9% move |
| GRT | SHORT | 0.93% | needs 0.9% move |
| AVAX | SHORT | 1.06% | needs 1.1% move; volume below average |

A trade needs **all four** of: price breaking its 3-day range, the trend filter agreeing, enough momentum (ADX over 20), and above-average volume. A coin at 0.00% that still has not traded is being held back by one of the other three — the table says which.

![market backdrop](chart-mood.svg)

## Results

![wins vs losses](chart-winloss.svg)

### Last 15 finished trades

| Coin | Direction | Result | Why it closed | When |
|---|---|---|---|---|
| BTC | SHORT | 🔴 -0.1855 (-12.2%) | stop_loss | 2026-09-15 17:33 |
| LINK | SHORT | 🔴 -0.1837 (-16.5%) | trailing_stop_loss | 2026-09-14 02:10 |
| QTUM | LONG | 🔴 -0.2246 (-20.2%) | stop_loss | 2026-09-12 16:06 |
| BCH | SHORT | 🟢 +0.4651 (+63.3%) | force_exit | 2026-09-10 13:25 |
| MANA | SHORT | 🔴 -0.2237 (-22.1%) | trailing_stop_loss | 2026-09-11 12:37 |
| EGLD | LONG | 🔴 -0.2262 (-42.6%) | stop_loss | 2026-09-10 11:05 |
| CRV | SHORT | 🔴 -0.2182 (-34.4%) | trailing_stop_loss | 2026-09-10 14:26 |
| AAVE | SHORT | 🟢 +0.2033 (+23.1%) | force_exit | 2026-09-10 11:07 |
| ALGO | LONG | 🟢 +0.1357 (+19.3%) | force_exit | 2026-09-08 16:07 |
| ATOM | LONG | 🟢 +0.4604 (+54.2%) | force_exit | 2026-09-08 16:07 |
| ETC | LONG | 🟢 +0.3342 (+50.9%) | force_exit | 2026-09-08 16:07 |
| DOT | LONG | 🟢 +0.4297 (+100.5%) | force_exit | 2026-09-08 16:07 |
| UNI | LONG | 🔴 -0.0737 (-10.9%) | force_exit | 2026-09-05 17:25 |
| SUSHI | LONG | 🟢 +0.8701 (+120.0%) | force_exit | 2026-09-05 17:24 |
| DOT | LONG | 🟢 +0.3555 (+55.3%) | force_exit | 2026-09-06 14:09 |

---

### How it works

Watches 47 coins every hour. Goes long when one breaks above its 3-day high, short when one breaks below its 3-day low — but only if the trend, momentum and volume all agree.

Every trade gets a stop-loss. Winners are left to run on a trailing stop rather than closed at a fixed target. It risks 1% of the account per trade and never holds more than 5 positions on the same side, so one bad day cannot end it.

**It loses more trades than it wins** — about 2-3 winners in 10, by design, with the winners much larger. Backtested on 2024-2026 it lost money. This is running on live prices with fake money to see what it actually does.
