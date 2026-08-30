# Hourly Trading Bot

**Updated 2026-08-30 14:07 UTC** &nbsp;·&nbsp; refreshes itself every hour

Paper money. $20 simulated, real Gate.io prices, no API keys — it cannot place a real order.

## Money

| | |
|---|---|
| **Equity now** | **$19.2370** 🔴 -3.82% |
| Settled balance | $18.6523 (-6.74%) |
| Unrealised (open trades) | 🟢 +0.5847 |
| Started with | $20.0000 |
| Finished trades | 7 |
| Open now | 5 |
| Win rate | 0% (0/7) |

![balance](chart-equity.svg)

## Open right now

| Coin | Direction | Entry | Price now | Moved | P&L | on margin | Room to stop |
|---|---|---|---|---|---|---|---|
| **FIL** | SHORT 🔻 | 0.6813 | 0.6853 | +0.59% | 🔴 -0.0476 | -6.7% | 2.12% |
| **SAND** | SHORT 🔻 | 0.03898 | 0.03924 | +0.67% | 🔴 -0.0948 | -13.5% | 2.04% |
| **EGLD** | LONG 🔺 | 3.622 | 3.831 | +5.77% | 🟢 +0.4704 | +56.5% | 0.91% |
| **UNI** | LONG 🔺 | 4.879 | 5.18 | +6.17% | 🟢 +0.2957 | +60.6% | 5.69% |
| **KSM** | LONG 🔺 | 3.636 | 3.627 | -0.25% | 🔴 -0.0390 | -3.5% | 1.38% |
| | | | | **total** | **+0.5847** | | |

> 3 long / 2 short · gross exposure **207% of equity**.

![FIL](pos-FIL.png)

![SAND](pos-SAND.png)

![EGLD](pos-EGLD.png)

![UNI](pos-UNI.png)

![KSM](pos-KSM.png)


## What it is waiting for

**0 coin(s) ready to fire right now.** Scanned 47 coins.

![closest to entry](chart-closest.svg)

![what is blocking entries](chart-blockers.svg)

| Coin | Would be | Needs | Status |
|---|---|---|---|
| UNI | LONG | 0.33% | needs 0.3% move |
| KSM | LONG | 0.66% | needs 0.7% move; volume below average |
| STORJ | SHORT | 0.90% | needs 0.9% move; volume below average |
| QTUM | SHORT | 0.95% | needs 1.0% move; trend too weak (ADX 9/20) |
| RVN | SHORT | 1.11% | needs 1.1% move; trend too weak (ADX 15/20) |
| CELO | LONG | 1.35% | needs 1.3% move |
| SNX | SHORT | 2.04% | needs 2.0% move; volume below average |
| ANKR | LONG | 2.08% | needs 2.1% move; trend too weak (ADX 12/20) |
| ALGO | SHORT | 2.21% | needs 2.2% move; trend too weak (ADX 18/20) |
| AVAX | LONG | 2.26% | needs 2.3% move; trend too weak (ADX 19/20) |

A trade needs **all four** of: price breaking its 3-day range, the trend filter agreeing, enough momentum (ADX over 20), and above-average volume. A coin at 0.00% that still has not traded is being held back by one of the other three — the table says which.

![market backdrop](chart-mood.svg)

## Results

![wins vs losses](chart-winloss.svg)

### Last 15 finished trades

| Coin | Direction | Result | Why it closed | When |
|---|---|---|---|---|
| THETA | SHORT | 🔴 -0.2014 (-14.1%) | stop_loss | 2026-08-30 06:59 |
| MANA | LONG | 🔴 -0.2131 (-17.8%) | stop_loss | 2026-08-30 04:42 |
| CRV | SHORT | 🔴 -0.1984 (-19.6%) | stop_loss | 2026-08-30 12:09 |
| ICP | LONG | 🔴 -0.2062 (-24.6%) | stop_loss | 2026-08-30 01:13 |
| BCH | SHORT | 🔴 -0.1922 (-19.8%) | trailing_stop_loss | 2026-08-29 20:06 |
| AXS | SHORT | 🔴 -0.1948 (-25.3%) | trailing_stop_loss | 2026-08-30 12:07 |
| UNI | LONG | 🔴 -0.1416 (-30.3%) | trailing_stop_loss | 2026-08-28 10:07 |

---

### How it works

Watches 47 coins every hour. Goes long when one breaks above its 3-day high, short when one breaks below its 3-day low — but only if the trend, momentum and volume all agree.

Every trade gets a stop-loss. Winners are left to run on a trailing stop rather than closed at a fixed target. It risks 1% of the account per trade and never holds more than 5 positions on the same side, so one bad day cannot end it.

**It loses more trades than it wins** — about 2-3 winners in 10, by design, with the winners much larger. Backtested on 2024-2026 it lost money. This is running on live prices with fake money to see what it actually does.
