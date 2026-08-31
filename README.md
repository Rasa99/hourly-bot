# Hourly Trading Bot

**Updated 2026-08-31 17:10 UTC** &nbsp;·&nbsp; refreshes itself every hour

Paper money. $20 simulated, real Gate.io prices, no API keys — it cannot place a real order.

## Money

| | |
|---|---|
| **Equity now** | **$19.0134** 🔴 -4.93% |
| Settled balance | $18.8169 (-5.92%) |
| Unrealised (open trades) | 🟢 +0.1964 |
| Started with | $20.0000 |
| Finished trades | 11 |
| Open now | 2 |
| Win rate | 18% (2/11) |

![balance](chart-equity.svg)

## Open right now

| Coin | Direction | Entry | Price now | Moved | P&L | on margin | Room to stop |
|---|---|---|---|---|---|---|---|
| **FIL** | SHORT 🔻 | 0.6813 | 0.6723 | -1.32% | 🟢 +0.0860 | +12.1% | 4.09% |
| **SAND** | SHORT 🔻 | 0.03898 | 0.03787 | -2.85% | 🟢 +0.1104 | +15.7% | 4.20% |
| | | | | **total** | **+0.1964** | | |

> ⚠️ **All 2 positions are short.** That is one bet on the same market direction, placed 2 times — these coins move together, so they will win together and lose together. Gross exposure is **75% of equity**.

![FIL](pos-FIL.png)

![SAND](pos-SAND.png)


## What it is waiting for

**1 coin(s) ready to fire right now.** Scanned 47 coins.

![closest to entry](chart-closest.svg)

![what is blocking entries](chart-blockers.svg)

| Coin | Would be | Needs | Status |
|---|---|---|---|
| DASH | LONG | 0.00% | **READY** |
| HBAR | SHORT | 0.53% | needs 0.5% move; volume below average |
| LRC | SHORT | 0.76% | needs 0.8% move; trend too weak (ADX 16/20) |
| BTC | LONG | 0.98% | needs 1.0% move; trend too weak (ADX 18/20) |
| LTC | SHORT | 1.99% | needs 2.0% move; volume below average |
| STORJ | SHORT | 2.06% | needs 2.1% move |
| ALGO | SHORT | 2.10% | needs 2.1% move; volume below average |
| BNB | LONG | 2.19% | needs 2.2% move; volume below average |
| ATOM | SHORT | 2.25% | needs 2.3% move; trend too weak (ADX 19/20) |
| THETA | SHORT | 2.33% | needs 2.3% move; volume below average |

A trade needs **all four** of: price breaking its 3-day range, the trend filter agreeing, enough momentum (ADX over 20), and above-average volume. A coin at 0.00% that still has not traded is being held back by one of the other three — the table says which.

![market backdrop](chart-mood.svg)

## Results

![wins vs losses](chart-winloss.svg)

### Last 15 finished trades

| Coin | Direction | Result | Why it closed | When |
|---|---|---|---|---|
| DASH | LONG | 🔴 -0.1861 (-35.0%) | stop_loss | 2026-08-30 20:43 |
| KSM | LONG | 🔴 -0.2021 (-17.9%) | stop_loss | 2026-08-30 20:40 |
| THETA | SHORT | 🔴 -0.2014 (-14.1%) | stop_loss | 2026-08-30 06:59 |
| MANA | LONG | 🔴 -0.2131 (-17.8%) | stop_loss | 2026-08-30 04:42 |
| UNI | LONG | 🟢 +0.1705 (+34.9%) | trailing_stop_loss | 2026-08-30 23:46 |
| CRV | SHORT | 🔴 -0.1984 (-19.6%) | stop_loss | 2026-08-30 12:09 |
| EGLD | LONG | 🟢 +0.3823 (+45.9%) | trailing_stop_loss | 2026-08-30 17:24 |
| ICP | LONG | 🔴 -0.2062 (-24.6%) | stop_loss | 2026-08-30 01:13 |
| BCH | SHORT | 🔴 -0.1922 (-19.8%) | trailing_stop_loss | 2026-08-29 20:06 |
| AXS | SHORT | 🔴 -0.1948 (-25.3%) | trailing_stop_loss | 2026-08-30 12:07 |
| UNI | LONG | 🔴 -0.1416 (-30.3%) | trailing_stop_loss | 2026-08-28 10:07 |

---

### How it works

Watches 47 coins every hour. Goes long when one breaks above its 3-day high, short when one breaks below its 3-day low — but only if the trend, momentum and volume all agree.

Every trade gets a stop-loss. Winners are left to run on a trailing stop rather than closed at a fixed target. It risks 1% of the account per trade and never holds more than 5 positions on the same side, so one bad day cannot end it.

**It loses more trades than it wins** — about 2-3 winners in 10, by design, with the winners much larger. Backtested on 2024-2026 it lost money. This is running on live prices with fake money to see what it actually does.
