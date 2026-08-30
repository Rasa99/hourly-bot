# Hourly Trading Bot

**Updated 2026-08-30 21:10 UTC** &nbsp;·&nbsp; refreshes itself every hour

Paper money. $20 simulated, real Gate.io prices, no API keys — it cannot place a real order.

## Money

| | |
|---|---|
| **Equity now** | **$19.1349** 🔴 -4.33% |
| Settled balance | $18.6465 (-6.77%) |
| Unrealised (open trades) | 🟢 +0.4884 |
| Started with | $20.0000 |
| Finished trades | 10 |
| Open now | 3 |
| Win rate | 10% (1/10) |

![balance](chart-equity.svg)

## Open right now

| Coin | Direction | Entry | Price now | Moved | P&L | on margin | Room to stop |
|---|---|---|---|---|---|---|---|
| **FIL** | SHORT 🔻 | 0.6813 | 0.6802 | -0.16% | 🟢 +0.0056 | +0.8% | 2.88% |
| **SAND** | SHORT 🔻 | 0.03898 | 0.0382 | -2.00% | 🟢 +0.0884 | +12.6% | 4.82% |
| **UNI** | LONG 🔺 | 4.879 | 5.279 | +8.20% | 🟢 +0.3943 | +80.8% | 4.19% |
| | | | | **total** | **+0.4884** | | |

> 1 long / 2 short · gross exposure **102% of equity**.

![FIL](pos-FIL.png)

![SAND](pos-SAND.png)

![UNI](pos-UNI.png)


## What it is waiting for

**1 coin(s) ready to fire right now.** Scanned 47 coins.

![closest to entry](chart-closest.svg)

![what is blocking entries](chart-blockers.svg)

| Coin | Would be | Needs | Status |
|---|---|---|---|
| SNX | SHORT | 0.00% | **READY** |
| STORJ | SHORT | 0.00% | volume below average |
| ETC | SHORT | 0.01% | needs 0.0% move |
| ENJ | SHORT | 0.32% | needs 0.3% move; trend too weak (ADX 18/20) |
| RVN | SHORT | 0.47% | needs 0.5% move; trend too weak (ADX 16/20) |
| QTUM | SHORT | 0.84% | needs 0.8% move; trend too weak (ADX 11/20) |
| ADA | SHORT | 1.09% | needs 1.1% move |
| DOGE | SHORT | 1.59% | needs 1.6% move; trend too weak (ADX 20/20) |
| SKL | SHORT | 1.62% | needs 1.6% move; trend too weak (ADX 14/20) |
| GALA | SHORT | 1.78% | needs 1.8% move; trend too weak (ADX 10/20) |

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
