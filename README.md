# Hourly Trading Bot

**Updated 2026-09-16 17:07 UTC** &nbsp;·&nbsp; refreshes itself every hour

Paper money. $20 simulated, real Gate.io prices, no API keys — it cannot place a real order.

## Money

| | |
|---|---|
| **Equity now** | **$22.4417** 🟢 +12.21% |
| Settled balance | $21.0174 (+5.09%) |
| Unrealised (open trades) | 🟢 +1.4243 |
| Started with | $20.0000 |
| Finished trades | 33 |
| Open now | 5 |
| Win rate | 39% (13/33) |

![balance](chart-equity.svg)

## Open right now

| Coin | Direction | Entry | Price now | Moved | P&L | on margin | Room to stop |
|---|---|---|---|---|---|---|---|
| **RVN** | SHORT 🔻 | 0.002126 | 0.002023 | -4.84% | 🟢 +0.3641 | +45.8% | 7.86% |
| **ICP** | SHORT 🔻 | 2.557 | 2.457 | -3.91% | 🟢 +0.2917 | +38.0% | 6.92% |
| **CRV** | SHORT 🔻 | 0.3239 | 0.3027 | -6.55% | 🟢 +0.3551 | +64.9% | 11.07% |
| **AAVE** | SHORT 🔻 | 120.91 | 115.31 | -4.63% | 🟢 +0.2749 | +45.5% | 7.99% |
| **BAND** | SHORT 🔻 | 0.1769 | 0.175 | -1.07% | 🟢 +0.1385 | +9.8% | 2.57% |
| | | | | **total** | **+1.4243** | | |

> ⚠️ **All 5 positions are short.** That is one bet on the same market direction, placed 5 times — these coins move together, so they will win together and lose together. Gross exposure is **196% of equity**.

![RVN](pos-RVN.png)

![ICP](pos-ICP.png)

![CRV](pos-CRV.png)

![AAVE](pos-AAVE.png)

![BAND](pos-BAND.png)


## What it is waiting for

**0 coin(s) ready to fire right now.** Scanned 47 coins.

![closest to entry](chart-closest.svg)

![what is blocking entries](chart-blockers.svg)

| Coin | Would be | Needs | Status |
|---|---|---|---|
| AAVE | SHORT | 0.00% | volume below average |
| CRV | SHORT | 0.00% | RSI already stretched (20/22) |
| BAND | SHORT | 0.00% | volume below average |
| KSM | SHORT | 0.06% | needs 0.1% move |
| ENJ | SHORT | 0.08% | needs 0.1% move; volume below average |
| EGLD | SHORT | 0.08% | needs 0.1% move |
| AXS | SHORT | 0.21% | needs 0.2% move |
| CHZ | SHORT | 0.30% | needs 0.3% move; volume below average |
| ATOM | SHORT | 0.34% | needs 0.3% move |
| BAT | SHORT | 0.56% | needs 0.6% move; volume below average |

A trade needs **all four** of: price breaking its 3-day range, the trend filter agreeing, enough momentum (ADX over 20), and above-average volume. A coin at 0.00% that still has not traded is being held back by one of the other three — the table says which.

![market backdrop](chart-mood.svg)

## Results

![wins vs losses](chart-winloss.svg)

### Last 15 finished trades

| Coin | Direction | Result | Why it closed | When |
|---|---|---|---|---|
| DOT | SHORT | 🔴 -0.2029 (-30.4%) | stop_loss | 2026-09-16 12:22 |
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

---

### How it works

Watches 47 coins every hour. Goes long when one breaks above its 3-day high, short when one breaks below its 3-day low — but only if the trend, momentum and volume all agree.

Every trade gets a stop-loss. Winners are left to run on a trailing stop rather than closed at a fixed target. It risks 1% of the account per trade and never holds more than 5 positions on the same side, so one bad day cannot end it.

**It loses more trades than it wins** — about 2-3 winners in 10, by design, with the winners much larger. Backtested on 2024-2026 it lost money. This is running on live prices with fake money to see what it actually does.
