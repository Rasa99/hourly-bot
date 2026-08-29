# Hourly Trading Bot

**Updated 2026-08-29 19:55 UTC** &nbsp;·&nbsp; refreshes itself every hour

Paper money. $20 simulated, real Gate.io prices, no API keys — it cannot place a real order.

## Money

| | |
|---|---|
| **Equity now** | **$19.6091** 🔴 -1.95% |
| Settled balance | $19.8584 (-0.71%) |
| Unrealised (open trades) | 🔴 -0.2493 |
| Started with | $20.0000 |
| Finished trades | 1 |
| Open now | 5 |
| Win rate | 0% (0/1) |

![balance](chart-equity.svg)

## Open right now

| Coin | Direction | Entry | Price now | Moved | P&L | on margin | Room to stop |
|---|---|---|---|---|---|---|---|
| **FIL** | SHORT 🔻 | 0.6813 | 0.6801 | -0.18% | 🟢 +0.0055 | +0.8% | 2.90% |
| **SAND** | SHORT 🔻 | 0.03898 | 0.03864 | -0.87% | 🟢 +0.0317 | +4.5% | 3.62% |
| **AXS** | SHORT 🔻 | 0.895 | 0.9016 | +0.74% | 🔴 -0.0622 | -8.1% | 1.73% |
| **BCH** | SHORT 🔻 | 243.04 | 247.01 | +1.63% | 🔴 -0.1686 | -17.3% | 0.20% |
| **ICP** | LONG 🔺 | 2.518 | 2.504 | -0.56% | 🔴 -0.0558 | -6.7% | 1.80% |
| | | | | **total** | **-0.2493** | | |

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
| SNX | SHORT | 0.58% | needs 0.6% move; volume below average |
| DOT | SHORT | 0.95% | needs 1.0% move; volume below average |
| ADA | SHORT | 1.00% | needs 1.0% move; volume below average |
| ICP | LONG | 1.15% | needs 1.2% move; volume below average |
| EGLD | LONG | 1.49% | needs 1.5% move; trend too weak (ADX 17/20) |
| DASH | LONG | 1.55% | needs 1.5% move |
| RVN | SHORT | 1.70% | needs 1.7% move; trend too weak (ADX 13/20) |
| BCH | SHORT | 1.80% | needs 1.8% move; volume below average |
| ENJ | SHORT | 1.83% | needs 1.8% move |
| SAND | SHORT | 1.87% | needs 1.9% move; volume below average |

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
