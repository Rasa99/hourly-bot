# Hourly Trading Bot

**Updated 2026-09-20 16:07 UTC** &nbsp;·&nbsp; refreshes itself every hour

Paper money. $20 simulated, real Gate.io prices, no API keys — it cannot place a real order.

## Money

| | |
|---|---|
| **Equity now** | **$20.9557** 🟢 +4.78% |
| Settled balance | $21.0630 (+5.32%) |
| Unrealised (open trades) | 🔴 -0.1073 |
| Started with | $20.0000 |
| Finished trades | 43 |
| Open now | 2 |
| Win rate | 37% (16/43) |

![balance](chart-equity.svg)

## Open right now

| Coin | Direction | Entry | Price now | Moved | P&L | on margin | Room to stop |
|---|---|---|---|---|---|---|---|
| **HBAR** | LONG 🔺 | 0.08775 | 0.08656 | -1.36% | 🔴 -0.0900 | -14.7% | 1.77% |
| **ALGO** | LONG 🔺 | 0.11309 | 0.11277 | -0.28% | 🔴 -0.0173 | -3.8% | 3.83% |
| | | | | **total** | **-0.1073** | | |

> ⚠️ **All 2 positions are long.** That is one bet on the same market direction, placed 2 times — these coins move together, so they will win together and lose together. Gross exposure is **51% of equity**.

![HBAR](pos-HBAR.png)

![ALGO](pos-ALGO.png)


## What it is waiting for

**1 coin(s) ready to fire right now.** Scanned 47 coins.

![closest to entry](chart-closest.svg)

![what is blocking entries](chart-blockers.svg)

| Coin | Would be | Needs | Status |
|---|---|---|---|
| AVAX | LONG | 0.00% | RSI already stretched (80/78) |
| ALGO | LONG | 0.00% | **READY** |
| GRT | LONG | 0.00% | trend too weak (ADX 19/20) |
| NEAR | LONG | 0.13% | needs 0.1% move |
| BTC | LONG | 1.29% | needs 1.3% move |
| ATOM | LONG | 1.66% | needs 1.7% move |
| IOTA | LONG | 1.85% | needs 1.8% move |
| EGLD | SHORT | 2.03% | needs 2.0% move |
| ETH | LONG | 2.18% | needs 2.2% move |
| BNB | LONG | 2.18% | needs 2.2% move; volume below average |

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
