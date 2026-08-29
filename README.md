# Hourly Trading Bot

**Updated 2026-08-29 16:12 UTC** &nbsp;·&nbsp; refreshes itself every hour

Paper money. $20 simulated, real Gate.io prices, no API keys — it cannot place a real order.

## Money

| | |
|---|---|
| **Equity now** | **$19.7891** 🔴 -1.05% |
| Settled balance | $19.8584 (-0.71%) |
| Unrealised (open trades) | 🔴 -0.0693 |
| Started with | $20.0000 |
| Finished trades | 1 |
| Open now | 5 |
| Win rate | 0% (0/1) |

![balance](chart-equity.svg)

## Open right now

| Coin | Direction | Entry | Price now | Moved | P&L | on margin | Room to stop |
|---|---|---|---|---|---|---|---|
| **FIL** | SHORT 🔻 | 0.6813 | 0.6842 | +0.43% | 🔴 -0.0302 | -4.3% | 2.28% |
| **SAND** | SHORT 🔻 | 0.03898 | 0.03848 | -1.28% | 🟢 +0.0900 | +12.8% | 4.05% |
| **AXS** | SHORT 🔻 | 0.895 | 0.9038 | +0.98% | 🔴 -0.0757 | -9.8% | 1.48% |
| **BCH** | SHORT 🔻 | 243.04 | 245.54 | +1.03% | 🔴 -0.1000 | -10.3% | 0.80% |
| **ICP** | LONG 🔺 | 2.518 | 2.532 | +0.56% | 🟢 +0.0466 | +5.6% | 2.88% |
| | | | | **total** | **-0.0693** | | |

> 1 long / 4 short · gross exposure **201% of equity**.

![FIL](pos-FIL.png)

![SAND](pos-SAND.png)

![AXS](pos-AXS.png)

![BCH](pos-BCH.png)

![ICP](pos-ICP.png)


## What it is waiting for

**0 coin(s) ready to fire right now.** Scanned 47 coins.

![closest to entry](chart-closest.svg)

![what is blocking entries](chart-blockers.svg)

| Coin | Would be | Needs | Status |
|---|---|---|---|
| BAND | LONG | 0.00% | trend too weak (ADX 17/20) |
| DASH | LONG | 0.14% | needs 0.1% move; volume below average |
| ICP | LONG | 0.43% | needs 0.4% move; volume below average |
| SNX | SHORT | 0.67% | needs 0.7% move; volume below average |
| ADA | SHORT | 0.95% | needs 0.9% move; volume below average |
| SAND | SHORT | 1.17% | needs 1.2% move |
| BCH | SHORT | 1.25% | needs 1.3% move; volume below average |
| DOT | SHORT | 1.31% | needs 1.3% move; volume below average |
| IOTA | SHORT | 1.56% | needs 1.6% move; volume below average |
| RVN | SHORT | 1.60% | needs 1.6% move; trend too weak (ADX 13/20) |

A trade needs **all four** of: price breaking its 3-day range, the trend filter agreeing, enough momentum (ADX over 20), and above-average volume. A coin at 0.00% that still has not traded is being held back by one of the other three — the table says which.

![market backdrop](chart-mood.svg)

## Results

![wins vs losses](chart-winloss.svg)

### Last 15 finished trades

| Coin | Direction | Result | Why it closed | When |
|---|---|---|---|---|
| UNI | LONG | 🔴 -0.1416 (-30.3%) | trailing_stop_loss | 2026-08-28 10:07 |

---

### How it works

Watches 47 coins every hour. Goes long when one breaks above its 3-day high, short when one breaks below its 3-day low — but only if the trend, momentum and volume all agree.

Every trade gets a stop-loss. Winners are left to run on a trailing stop rather than closed at a fixed target. It risks 1% of the account per trade and never holds more than 5 positions on the same side, so one bad day cannot end it.

**It loses more trades than it wins** — about 2-3 winners in 10, by design, with the winners much larger. Backtested on 2024-2026 it lost money. This is running on live prices with fake money to see what it actually does.
