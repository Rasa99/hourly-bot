# Hourly Trading Bot

**Updated 2026-08-30 16:10 UTC** &nbsp;·&nbsp; refreshes itself every hour

Paper money. $20 simulated, real Gate.io prices, no API keys — it cannot place a real order.

## Money

| | |
|---|---|
| **Equity now** | **$19.3134** 🔴 -3.43% |
| Settled balance | $18.6523 (-6.74%) |
| Unrealised (open trades) | 🟢 +0.6611 |
| Started with | $20.0000 |
| Finished trades | 7 |
| Open now | 5 |
| Win rate | 0% (0/7) |

![balance](chart-equity.svg)

## Open right now

| Coin | Direction | Entry | Price now | Moved | P&L | on margin | Room to stop |
|---|---|---|---|---|---|---|---|
| **FIL** | SHORT 🔻 | 0.6813 | 0.6836 | +0.34% | 🔴 -0.0298 | -4.2% | 2.37% |
| **SAND** | SHORT 🔻 | 0.03898 | 0.03934 | +0.92% | 🔴 -0.1169 | -16.7% | 1.78% |
| **EGLD** | LONG 🔺 | 3.622 | 3.866 | +6.74% | 🟢 +0.5501 | +66.0% | 1.81% |
| **UNI** | LONG 🔺 | 4.879 | 5.208 | +6.74% | 🟢 +0.3234 | +66.3% | 6.20% |
| **KSM** | LONG 🔺 | 3.636 | 3.618 | -0.50% | 🔴 -0.0658 | -5.8% | 1.13% |
| | | | | **total** | **+0.6611** | | |

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
| KSM | LONG | 0.41% | needs 0.4% move; volume below average |
| SNX | SHORT | 1.10% | needs 1.1% move |
| QTUM | SHORT | 1.21% | needs 1.2% move; trend too weak (ADX 9/20) |
| RVN | SHORT | 1.27% | needs 1.3% move; trend too weak (ADX 14/20) |
| HBAR | SHORT | 1.60% | needs 1.6% move; trend too weak (ADX 16/20) |
| CELO | LONG | 1.74% | needs 1.7% move; volume below average |
| STORJ | SHORT | 1.87% | needs 1.9% move |
| ADA | SHORT | 2.16% | needs 2.2% move |
| ETH | LONG | 2.18% | needs 2.2% move |
| ALGO | SHORT | 2.21% | needs 2.2% move; trend too weak (ADX 16/20) |

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
