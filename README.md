# Hourly Trading Bot

**Updated 2026-09-15 22:07 UTC** &nbsp;·&nbsp; refreshes itself every hour

Paper money. $20 simulated, real Gate.io prices, no API keys — it cannot place a real order.

## Money

| | |
|---|---|
| **Equity now** | **$21.8970** 🟢 +9.48% |
| Settled balance | $21.2203 (+6.10%) |
| Unrealised (open trades) | 🟢 +0.6767 |
| Started with | $20.0000 |
| Finished trades | 32 |
| Open now | 5 |
| Win rate | 41% (13/32) |

![balance](chart-equity.svg)

## Open right now

| Coin | Direction | Entry | Price now | Moved | P&L | on margin | Room to stop |
|---|---|---|---|---|---|---|---|
| **RVN** | SHORT 🔻 | 0.002126 | 0.002074 | -2.45% | 🟢 +0.1809 | +22.8% | 5.21% |
| **ICP** | SHORT 🔻 | 2.557 | 2.458 | -3.87% | 🟢 +0.2892 | +37.7% | 6.88% |
| **DOT** | SHORT 🔻 | 0.953 | 0.942 | -1.15% | 🟢 +0.0704 | +10.5% | 4.14% |
| **CRV** | SHORT 🔻 | 0.3239 | 0.3147 | -2.84% | 🟢 +0.1533 | +28.0% | 6.83% |
| **AAVE** | SHORT 🔻 | 120.91 | 121.13 | +0.18% | 🔴 -0.0171 | -2.8% | 2.80% |
| | | | | **total** | **+0.6767** | | |

> ⚠️ **All 5 positions are short.** That is one bet on the same market direction, placed 5 times — these coins move together, so they will win together and lose together. Gross exposure is **159% of equity**.

![RVN](pos-RVN.png)

![ICP](pos-ICP.png)

![DOT](pos-DOT.png)

![CRV](pos-CRV.png)

![AAVE](pos-AAVE.png)


## What it is waiting for

**2 coin(s) ready to fire right now.** Scanned 47 coins.

![closest to entry](chart-closest.svg)

![what is blocking entries](chart-blockers.svg)

| Coin | Would be | Needs | Status |
|---|---|---|---|
| ALGO | SHORT | 0.00% | trend too weak (ADX 20/20); volume below average |
| AAVE | SHORT | 0.00% | **READY** |
| CRV | SHORT | 0.00% | volume below average |
| EGLD | SHORT | 0.00% | **READY** |
| BAND | SHORT | 0.17% | needs 0.2% move; volume below average |
| ICP | SHORT | 0.20% | needs 0.2% move; volume below average |
| GRT | SHORT | 0.29% | needs 0.3% move |
| ATOM | SHORT | 0.33% | needs 0.3% move |
| LTC | SHORT | 0.35% | needs 0.4% move; volume below average |
| BNB | SHORT | 0.49% | needs 0.5% move; trend too weak (ADX 17/20) |

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
