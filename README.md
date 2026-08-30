# Hourly Trading Bot

**Updated 2026-08-30 22:07 UTC** &nbsp;·&nbsp; refreshes itself every hour

Paper money. $20 simulated, real Gate.io prices, no API keys — it cannot place a real order.

## Money

| | |
|---|---|
| **Equity now** | **$19.0652** 🔴 -4.67% |
| Settled balance | $18.6465 (-6.77%) |
| Unrealised (open trades) | 🟢 +0.4187 |
| Started with | $20.0000 |
| Finished trades | 10 |
| Open now | 3 |
| Win rate | 10% (1/10) |

![balance](chart-equity.svg)

## Open right now

| Coin | Direction | Entry | Price now | Moved | P&L | on margin | Room to stop |
|---|---|---|---|---|---|---|---|
| **FIL** | SHORT 🔻 | 0.6813 | 0.6841 | +0.41% | 🔴 -0.0350 | -4.9% | 2.29% |
| **SAND** | SHORT 🔻 | 0.03898 | 0.0386 | -0.97% | 🟢 +0.0164 | +2.3% | 3.73% |
| **UNI** | LONG 🔺 | 4.879 | 5.322 | +9.08% | 🟢 +0.4373 | +89.6% | 4.96% |
| | | | | **total** | **+0.4187** | | |

> 1 long / 2 short · gross exposure **102% of equity**.

![FIL](pos-FIL.png)

![SAND](pos-SAND.png)

![UNI](pos-UNI.png)


## What it is waiting for

**0 coin(s) ready to fire right now.** Scanned 47 coins.

![closest to entry](chart-closest.svg)

![what is blocking entries](chart-blockers.svg)

| Coin | Would be | Needs | Status |
|---|---|---|---|
| ENJ | SHORT | 0.00% | volume below average |
| STORJ | SHORT | 0.00% | volume below average |
| RVN | SHORT | 0.10% | needs 0.1% move; trend too weak (ADX 18/20) |
| ADA | SHORT | 0.65% | needs 0.6% move |
| ETC | SHORT | 0.68% | needs 0.7% move |
| QTUM | SHORT | 0.84% | needs 0.8% move; trend too weak (ADX 11/20) |
| DOGE | SHORT | 0.99% | needs 1.0% move; trend too weak (ADX 20/20) |
| SAND | SHORT | 1.72% | needs 1.7% move |
| HBAR | SHORT | 1.73% | needs 1.7% move; trend too weak (ADX 16/20) |
| LRC | SHORT | 1.84% | needs 1.8% move; volume below average |

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
