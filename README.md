# Hourly Trading Bot

**Updated 2026-08-28 14:12 UTC** &nbsp;·&nbsp; refreshes itself every hour

Paper money. $20 simulated, real Gate.io prices, no API keys — it cannot place a real order.

## Money

| | |
|---|---|
| **Balance** | **$19.8584** 🔴 |
| Started with | $20.0000 |
| Change | -0.71% |
| Finished trades | 1 |
| Open now | 0 |
| Win rate | 0% (0/1) |

![balance](chart-equity.svg)

## Open right now

Nothing open.

## What it is waiting for

**0 coin(s) ready to fire right now.** Scanned 47 coins.

![closest to entry](chart-closest.svg)

![what is blocking entries](chart-blockers.svg)

| Coin | Would be | Needs | Status |
|---|---|---|---|
| AXS | SHORT | 0.00% | trend too weak (ADX 20/20) |
| SAND | SHORT | 0.08% | needs 0.1% move; volume below average |
| FIL | SHORT | 1.25% | needs 1.3% move; volume below average |
| BAT | LONG | 2.46% | needs 2.5% move |
| BNB | LONG | 2.73% | needs 2.7% move; trend too weak (ADX 18/20) |
| ETH | LONG | 3.42% | needs 3.4% move; trend too weak (ADX 9/20) |
| ANKR | LONG | 3.55% | needs 3.6% move; trend too weak (ADX 18/20) |
| BTC | LONG | 3.56% | needs 3.6% move; trend too weak (ADX 20/20) |
| AVAX | LONG | 3.66% | needs 3.7% move; trend too weak (ADX 18/20) |
| STORJ | SHORT | 3.71% | needs 3.7% move |

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
