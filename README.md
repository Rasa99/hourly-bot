# Hourly Trading Bot

**Updated 2026-09-17 17:07 UTC** &nbsp;·&nbsp; refreshes itself every hour

Paper money. $20 simulated, real Gate.io prices, no API keys — it cannot place a real order.

## Money

| | |
|---|---|
| **Equity now** | **$20.0078** 🟢 +0.04% |
| Settled balance | $20.3828 (+1.91%) |
| Unrealised (open trades) | 🔴 -0.3750 |
| Started with | $20.0000 |
| Finished trades | 36 |
| Open now | 2 |
| Win rate | 36% (13/36) |

![balance](chart-equity.svg)

## Open right now

| Coin | Direction | Entry | Price now | Moved | P&L | on margin | Room to stop |
|---|---|---|---|---|---|---|---|
| **ICP** | SHORT 🔻 | 2.557 | 2.613 | +2.19% | 🔴 -0.1756 | -22.9% | 0.54% |
| **CRV** | SHORT 🔻 | 0.3239 | 0.3356 | +3.61% | 🔴 -0.1994 | -36.4% | 0.18% |
| | | | | **total** | **-0.3750** | | |

> ⚠️ **All 2 positions are short.** That is one bet on the same market direction, placed 2 times — these coins move together, so they will win together and lose together. Gross exposure is **64% of equity**.

![ICP](pos-ICP.png)

![CRV](pos-CRV.png)


## What it is waiting for

**2 coin(s) ready to fire right now.** Scanned 47 coins.

![closest to entry](chart-closest.svg)

![what is blocking entries](chart-blockers.svg)

| Coin | Would be | Needs | Status |
|---|---|---|---|
| UNI | LONG | 0.00% | **READY** |
| NEAR | LONG | 0.00% | RSI already stretched (79/78) |
| DASH | LONG | 0.00% | **READY** |
| KSM | LONG | 0.00% | RSI already stretched (90/78) |
| BTC | SHORT | 2.38% | needs 2.4% move; trend too weak (ADX 14/20) |
| BNB | SHORT | 3.38% | needs 3.4% move; trend too weak (ADX 19/20) |
| QTUM | SHORT | 4.36% | needs 4.4% move; trend too weak (ADX 16/20) |
| ONT | SHORT | 4.53% | needs 4.5% move; trend too weak (ADX 18/20) |
| ETH | SHORT | 4.57% | needs 4.6% move; volume below average |
| DOGE | SHORT | 4.62% | needs 4.6% move; trend too weak (ADX 19/20) |

A trade needs **all four** of: price breaking its 3-day range, the trend filter agreeing, enough momentum (ADX over 20), and above-average volume. A coin at 0.00% that still has not traded is being held back by one of the other three — the table says which.

![market backdrop](chart-mood.svg)

## Results

![wins vs losses](chart-winloss.svg)

### Last 15 finished trades

| Coin | Direction | Result | Why it closed | When |
|---|---|---|---|---|
| BAND | SHORT | 🔴 -0.2433 (-17.3%) | stop_loss | 2026-09-16 21:01 |
| AAVE | SHORT | 🔴 -0.1684 (-27.9%) | trailing_stop_loss | 2026-09-17 12:58 |
| DOT | SHORT | 🔴 -0.2029 (-30.4%) | stop_loss | 2026-09-16 12:22 |
| BTC | SHORT | 🔴 -0.1855 (-12.2%) | stop_loss | 2026-09-15 17:33 |
| RVN | SHORT | 🔴 -0.2229 (-28.0%) | trailing_stop_loss | 2026-09-17 06:14 |
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

---

### How it works

Watches 47 coins every hour. Goes long when one breaks above its 3-day high, short when one breaks below its 3-day low — but only if the trend, momentum and volume all agree.

Every trade gets a stop-loss. Winners are left to run on a trailing stop rather than closed at a fixed target. It risks 1% of the account per trade and never holds more than 5 positions on the same side, so one bad day cannot end it.

**It loses more trades than it wins** — about 2-3 winners in 10, by design, with the winners much larger. Backtested on 2024-2026 it lost money. This is running on live prices with fake money to see what it actually does.
