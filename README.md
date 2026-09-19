# Hourly Trading Bot

**Updated 2026-09-19 09:07 UTC** &nbsp;·&nbsp; refreshes itself every hour

Paper money. $20 simulated, real Gate.io prices, no API keys — it cannot place a real order.

## Money

| | |
|---|---|
| **Equity now** | **$20.9849** 🟢 +4.92% |
| Settled balance | $19.7755 (-1.12%) |
| Unrealised (open trades) | 🟢 +1.2094 |
| Started with | $20.0000 |
| Finished trades | 39 |
| Open now | 4 |
| Win rate | 33% (13/39) |

![balance](chart-equity.svg)

## Open right now

| Coin | Direction | Entry | Price now | Moved | P&L | on margin | Room to stop |
|---|---|---|---|---|---|---|---|
| **AVAX** | LONG 🔺 | 8.209 | 8.881 | +8.19% | 🟢 +0.6618 | +80.6% | 5.97% |
| **FIL** | LONG 🔺 | 0.9162 | 0.973 | +6.20% | 🟢 +0.3741 | +60.8% | 6.63% |
| **ADA** | LONG 🔺 | 0.2238 | 0.2243 | +0.22% | 🟢 +0.0069 | +1.0% | 2.63% |
| **CELO** | LONG 🔺 | 0.0838 | 0.0851 | +1.55% | 🟢 +0.1666 | +14.3% | 3.18% |
| | | | | **total** | **+1.2094** | | |

> ⚠️ **All 4 positions are long.** That is one bet on the same market direction, placed 4 times — these coins move together, so they will win together and lose together. Gross exposure is **166% of equity**.

![AVAX](pos-AVAX.png)

![FIL](pos-FIL.png)

![ADA](pos-ADA.png)

![CELO](pos-CELO.png)


## What it is waiting for

**1 coin(s) ready to fire right now.** Scanned 47 coins.

![closest to entry](chart-closest.svg)

![what is blocking entries](chart-blockers.svg)

| Coin | Would be | Needs | Status |
|---|---|---|---|
| AVAX | LONG | 0.00% | **READY** |
| IOTA | LONG | 0.00% | volume below average; RSI already stretched (82/78) |
| ETH | LONG | 0.08% | needs 0.1% move |
| BNB | LONG | 0.43% | needs 0.4% move; volume below average |
| APE | LONG | 0.51% | needs 0.5% move; volume below average |
| CHZ | LONG | 0.53% | needs 0.5% move |
| BTC | LONG | 0.60% | needs 0.6% move; volume below average |
| LINK | LONG | 0.68% | needs 0.7% move; volume below average |
| ETC | LONG | 0.74% | needs 0.7% move |
| MANA | LONG | 0.96% | needs 1.0% move; volume below average |

A trade needs **all four** of: price breaking its 3-day range, the trend filter agreeing, enough momentum (ADX over 20), and above-average volume. A coin at 0.00% that still has not traded is being held back by one of the other three — the table says which.

![market backdrop](chart-mood.svg)

## Results

![wins vs losses](chart-winloss.svg)

### Last 15 finished trades

| Coin | Direction | Result | Why it closed | When |
|---|---|---|---|---|
| DASH | LONG | 🔴 -0.1733 (-45.7%) | stop_loss | 2026-09-19 05:58 |
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
| MANA | SHORT | 🔴 -0.2237 (-22.1%) | trailing_stop_loss | 2026-09-11 12:37 |
| EGLD | LONG | 🔴 -0.2262 (-42.6%) | stop_loss | 2026-09-10 11:05 |
| CRV | SHORT | 🔴 -0.2182 (-34.4%) | trailing_stop_loss | 2026-09-10 14:26 |
| AAVE | SHORT | 🟢 +0.2033 (+23.1%) | force_exit | 2026-09-10 11:07 |

---

### How it works

Watches 47 coins every hour. Goes long when one breaks above its 3-day high, short when one breaks below its 3-day low — but only if the trend, momentum and volume all agree.

Every trade gets a stop-loss. Winners are left to run on a trailing stop rather than closed at a fixed target. It risks 1% of the account per trade and never holds more than 5 positions on the same side, so one bad day cannot end it.

**It loses more trades than it wins** — about 2-3 winners in 10, by design, with the winners much larger. Backtested on 2024-2026 it lost money. This is running on live prices with fake money to see what it actually does.
