# Hourly Trading Bot

**Updated 2026-08-30 08:07 UTC** &nbsp;·&nbsp; refreshes itself every hour

Paper money. $20 simulated, real Gate.io prices, no API keys — it cannot place a real order.

## Money

| | |
|---|---|
| **Equity now** | **$19.1648** 🔴 -4.18% |
| Settled balance | $19.0456 (-4.77%) |
| Unrealised (open trades) | 🟢 +0.1193 |
| Started with | $20.0000 |
| Finished trades | 5 |
| Open now | 7 |
| Win rate | 0% (0/5) |

![balance](chart-equity.svg)

## Open right now

| Coin | Direction | Entry | Price now | Moved | P&L | on margin | Room to stop |
|---|---|---|---|---|---|---|---|
| **FIL** | SHORT 🔻 | 0.6813 | 0.6811 | -0.03% | 🔴 -0.0039 | -0.6% | 2.75% |
| **SAND** | SHORT 🔻 | 0.03898 | 0.03851 | -1.21% | 🟢 +0.0366 | +5.2% | 3.97% |
| **AXS** | SHORT 🔻 | 0.895 | 0.9066 | +1.30% | 🔴 -0.1036 | -13.5% | 1.17% |
| **EGLD** | LONG 🔺 | 3.622 | 3.793 | +4.72% | 🟢 +0.3831 | +46.0% | 5.46% |
| **CRV** | SHORT 🔻 | 0.2973 | 0.3 | +0.91% | 🔴 -0.0967 | -9.6% | 0.97% |
| **UNI** | LONG 🔺 | 4.879 | 4.892 | +0.27% | 🟢 +0.0078 | +1.6% | 3.09% |
| **KSM** | LONG 🔺 | 3.636 | 3.606 | -0.83% | 🔴 -0.1040 | -9.2% | 0.80% |
| | | | | **total** | **+0.1193** | | |

> 3 long / 4 short · gross exposure **296% of equity**.

![FIL](pos-FIL.png)

![SAND](pos-SAND.png)

![AXS](pos-AXS.png)

![EGLD](pos-EGLD.png)

![CRV](pos-CRV.png)

![UNI](pos-UNI.png)

![KSM](pos-KSM.png)


## What it is waiting for

**0 coin(s) ready to fire right now.** Scanned 47 coins.

![closest to entry](chart-closest.svg)

![what is blocking entries](chart-blockers.svg)

| Coin | Would be | Needs | Status |
|---|---|---|---|
| STORJ | SHORT | 0.79% | needs 0.8% move; volume below average |
| ADA | SHORT | 0.80% | needs 0.8% move; trend too weak (ADX 19/20) |
| THETA | SHORT | 0.89% | needs 0.9% move; volume below average |
| BCH | SHORT | 0.93% | needs 0.9% move |
| CRV | SHORT | 1.03% | needs 1.0% move; volume below average |
| KSM | LONG | 1.08% | needs 1.1% move; volume below average |
| EGLD | LONG | 1.11% | needs 1.1% move |
| DOT | SHORT | 1.31% | needs 1.3% move; trend too weak (ADX 20/20) |
| RVN | SHORT | 1.54% | needs 1.5% move; trend too weak (ADX 14/20) |
| HBAR | SHORT | 1.56% | needs 1.6% move; trend too weak (ADX 18/20) |

A trade needs **all four** of: price breaking its 3-day range, the trend filter agreeing, enough momentum (ADX over 20), and above-average volume. A coin at 0.00% that still has not traded is being held back by one of the other three — the table says which.

![market backdrop](chart-mood.svg)

## Results

![wins vs losses](chart-winloss.svg)

### Last 15 finished trades

| Coin | Direction | Result | Why it closed | When |
|---|---|---|---|---|
| THETA | SHORT | 🔴 -0.2014 (-14.1%) | stop_loss | 2026-08-30 06:59 |
| MANA | LONG | 🔴 -0.2131 (-17.8%) | stop_loss | 2026-08-30 04:42 |
| ICP | LONG | 🔴 -0.2062 (-24.6%) | stop_loss | 2026-08-30 01:13 |
| BCH | SHORT | 🔴 -0.1922 (-19.8%) | trailing_stop_loss | 2026-08-29 20:06 |
| UNI | LONG | 🔴 -0.1416 (-30.3%) | trailing_stop_loss | 2026-08-28 10:07 |

---

### How it works

Watches 47 coins every hour. Goes long when one breaks above its 3-day high, short when one breaks below its 3-day low — but only if the trend, momentum and volume all agree.

Every trade gets a stop-loss. Winners are left to run on a trailing stop rather than closed at a fixed target. It risks 1% of the account per trade and never holds more than 5 positions on the same side, so one bad day cannot end it.

**It loses more trades than it wins** — about 2-3 winners in 10, by design, with the winners much larger. Backtested on 2024-2026 it lost money. This is running on live prices with fake money to see what it actually does.
