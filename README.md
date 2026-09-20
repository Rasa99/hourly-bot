# Hourly Trading Bot

**Updated 2026-09-20 17:07 UTC** &nbsp;·&nbsp; refreshes itself every hour

Paper money. $20 simulated, real Gate.io prices, no API keys — it cannot place a real order.

## Money

| | |
|---|---|
| **Equity now** | **$21.0486** 🟢 +5.24% |
| Settled balance | $21.0630 (+5.32%) |
| Unrealised (open trades) | 🔴 -0.0145 |
| Started with | $20.0000 |
| Finished trades | 43 |
| Open now | 2 |
| Win rate | 37% (16/43) |

![balance](chart-equity.svg)

## Open right now

| Coin | Direction | Entry | Price now | Moved | P&L | on margin | Room to stop |
|---|---|---|---|---|---|---|---|
| **HBAR** | LONG 🔺 | 0.08775 | 0.08767 | -0.09% | 🔴 -0.0123 | -2.0% | 3.01% |
| **ALGO** | LONG 🔺 | 0.11309 | 0.11315 | +0.05% | 🔴 -0.0021 | -0.5% | 4.15% |
| | | | | **total** | **-0.0145** | | |

> ⚠️ **All 2 positions are long.** That is one bet on the same market direction, placed 2 times — these coins move together, so they will win together and lose together. Gross exposure is **51% of equity**.

![HBAR](pos-HBAR.png)

![ALGO](pos-ALGO.png)


## What it is waiting for

**0 coin(s) ready to fire right now.** Scanned 47 coins.

![closest to entry](chart-closest.svg)

![what is blocking entries](chart-blockers.svg)

| Coin | Would be | Needs | Status |
|---|---|---|---|
| NEAR | LONG | 0.00% | RSI already stretched (83/78) |
| LTC | LONG | 0.29% | needs 0.3% move |
| ATOM | LONG | 0.51% | needs 0.5% move |
| DOT | LONG | 0.52% | needs 0.5% move |
| BTC | LONG | 0.75% | needs 0.7% move |
| SAND | LONG | 0.83% | needs 0.8% move |
| IOTA | LONG | 0.87% | needs 0.9% move |
| LINK | LONG | 0.93% | needs 0.9% move |
| GRT | LONG | 0.97% | needs 1.0% move |
| BAT | LONG | 1.02% | needs 1.0% move |

A trade needs **all four** of: price breaking its 3-day range, the trend filter agreeing, enough momentum (ADX over 20), and above-average volume. A coin at 0.00% that still has not traded is being held back by one of the other three — the table says which.

![market backdrop](chart-mood.svg)

## Results

![wins vs losses](chart-winloss.svg)

### Last 15 finished trades

| Coin | Direction | Result | Why it closed | When |
|---|---|---|---|---|
| DASH | LONG | 🔴 -0.1733 (-45.7%) | stop_loss | 2026-09-19 05:58 |
| CELO | LONG | 🟢 +0.1347 (+11.6%) | force_exit | 2026-09-19 09:28 |
| ADA | LONG | 🔴 -0.0111 (-1.6%) | force_exit | 2026-09-19 09:28 |
| FIL | LONG | 🟢 +0.3452 (+56.0%) | force_exit | 2026-09-19 09:28 |
| AVAX | LONG | 🟢 +0.8187 (+99.7%) | force_exit | 2026-09-19 09:28 |
| BAND | SHORT | 🔴 -0.2433 (-17.3%) | stop_loss | 2026-09-16 21:01 |
| AAVE | SHORT | 🔴 -0.1684 (-27.9%) | trailing_stop_loss | 2026-09-17 12:58 |
| CRV | SHORT | 🔴 -0.2163 (-39.5%) | stop_loss | 2026-09-17 17:07 |
| DOT | SHORT | 🔴 -0.2029 (-30.4%) | stop_loss | 2026-09-16 12:22 |
| BTC | SHORT | 🔴 -0.1855 (-12.2%) | stop_loss | 2026-09-15 17:33 |
| ICP | SHORT | 🔴 -0.2177 (-28.4%) | stop_loss | 2026-09-17 18:20 |
| RVN | SHORT | 🔴 -0.2229 (-28.0%) | trailing_stop_loss | 2026-09-17 06:14 |
| LINK | SHORT | 🔴 -0.1837 (-16.5%) | trailing_stop_loss | 2026-09-14 02:10 |
| QTUM | LONG | 🔴 -0.2246 (-20.2%) | stop_loss | 2026-09-12 16:06 |
| BCH | SHORT | 🟢 +0.4651 (+63.3%) | force_exit | 2026-09-10 13:25 |

---

### How it works

Watches 47 coins every hour. Goes long when one breaks above its 3-day high, short when one breaks below its 3-day low — but only if the trend, momentum and volume all agree.

Every trade gets a stop-loss. Winners are left to run on a trailing stop rather than closed at a fixed target. It risks 1% of the account per trade and never holds more than 5 positions on the same side, so one bad day cannot end it.

**It loses more trades than it wins** — about 2-3 winners in 10, by design, with the winners much larger. Backtested on 2024-2026 it lost money. This is running on live prices with fake money to see what it actually does.
