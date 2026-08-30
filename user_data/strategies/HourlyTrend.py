"""
HourlyTrend — the fast version. Built because Rasa asked for it, having been
shown the slow-vs-fast numbers and decided anyway. That is a legitimate call:
he wants to watch it work rather than read about it.

It is the same engine as TrendFollower, retimed for the hour:

  Entry    breakout of the 72-hour (3 day) high or low, confirmed by an
           EMA trend filter and a volume check. Roughly 18x more entry
           opportunities than the 55-DAY breakout it replaces.
  Stop     2x ATR(20) from entry.
  Exit     chandelier trailing stop, 6x ATR - wide enough to let a winner run,
           scaled down from the daily version's 9x because an hourly ATR is a
           much smaller distance.
  Size     1% of equity risked per trade, same as before.
  Leverage derived per trade so liquidation can never precede the stop.
  Cap      max 5 positions per side, the correlation fix that turned the daily
           version's worst year from -35% to +2%.

Extra technicals Rasa asked for, all used as CONFIRMATION rather than as the
trigger - the breakout is still what fires the trade:
  - EMA(50)/EMA(200) trend alignment on the hour
  - RSI(14) not already exhausted at the moment of entry
  - volume above its 20-hour average, so it is a real move not a dead-hours wick
  - ADX(14) above a floor, so it only takes breakouts with some force behind
    them instead of every drift through a level

HONEST EXPECTATION, so nobody is surprised: everything measured in this project
says faster trading performs worse after costs - 5m -99.91%, 15m -91.9%,
1h -38.4%, 4h -2.6% on the earlier strategy family, and a 10-day breakout
scored +14% in training and -12% out of sample. This file exists to find out
what THIS engine does on the hour, with real numbers, not to promise it wins.
"""

import os
from datetime import datetime

import talib.abstract as ta
from pandas import DataFrame

from freqtrade.persistence import Trade
from freqtrade.strategy import (
    DecimalParameter,
    IntParameter,
    IStrategy,
    stoploss_from_absolute,
)


class HourlyTrend(IStrategy):
    INTERFACE_VERSION = 3

    timeframe = "1h"
    can_short = True
    process_only_new_candles = True
    use_custom_stoploss = True
    use_exit_signal = False          # the trailing stop is the exit

    minimal_roi = {"0": 100.0}       # no profit target - winners must be free to run
    stoploss = -0.60                 # safety net only; real stop is ATR based

    # 800, not 300. EMA is RECURSIVE - its value depends on every candle before
    # it - so with too little warmup it never converges and reads slightly
    # wrong. Measured with `freqtrade recursive-analysis`:
    #
    #   warmup:      200      300      400      800     1000
    #   ema_slow: -0.018%  +0.050%  +0.041%   0.000%  -0.000%
    #
    # 0.05% sounds trivial and is not: when price sits near the EMA it flips
    # the trend filter, which flips the trade. `lookahead-analysis` caught it
    # as real bias - 2 biased entries and 2 biased exits out of 20 signals,
    # while TrendFollower (which uses a non-recursive SMA) scored a clean zero.
    #
    # A backtest run with unconverged indicators is measuring a strategy that
    # could not have existed live. Do not lower this.
    startup_candle_count: int = 800

    # --- entry -----------------------------------------------------------
    breakout_hours = IntParameter(
        24, 240, default=int(os.environ.get("FT_BREAKOUT_H", "72")),
        space="buy", optimize=False,
    )
    ema_fast = IntParameter(20, 100, default=50, space="buy", optimize=False)
    ema_slow = IntParameter(100, 250, default=200, space="buy", optimize=False)
    adx_floor = IntParameter(10, 35, default=20, space="buy", optimize=False)
    rsi_long_max = IntParameter(60, 90, default=78, space="buy", optimize=False)
    rsi_short_min = IntParameter(10, 40, default=22, space="buy", optimize=False)

    # --- exits -----------------------------------------------------------
    initial_stop_atr = DecimalParameter(
        1.0, 6.0, default=float(os.environ.get("FT_STOP_ATR", "2.0")),
        space="sell", optimize=False,
    )
    trail_atr = DecimalParameter(
        2.0, 20.0, default=float(os.environ.get("FT_TRAIL_ATR", "6.0")),
        space="sell", optimize=False,
    )

    # --- risk ------------------------------------------------------------
    risk_per_trade = DecimalParameter(0.005, 0.02, default=0.01, space="sell", optimize=False)
    liq_safety_factor = 2.0
    hard_leverage_cap = float(os.environ.get("FT_LEVERAGE_CAP", "10"))
    force_leverage = float(os.environ.get("FT_FORCE_LEVERAGE", "0"))
    max_forced_risk = 0.05
    max_same_side = int(os.environ.get("FT_MAX_SAME_SIDE", "5"))

    # Cap on how many positions may be OPENED in a single candle.
    #
    # ADDED 2026-08-30, default 1. This is the only change tested this session
    # that was better in BOTH windows, and it was better on all three measures
    # at once (research/hourly_crowding_results.txt):
    #
    #                        TRAIN                    HOLDOUT
    #   no limit (before)    -73.05%  PF 0.72  DD 75%  -60.17%  PF 0.82  DD 79%
    #   max 1 per candle     -57.52%  PF 0.80  DD 64%  -12.06%  PF 0.97  DD 53%
    #
    # WHY. max_same_side limits how many correlated positions are HELD. It says
    # nothing about how fast they are acquired, and the live bot showed what
    # that costs on its second day (cloud/user_data/logs/cloud.log):
    #
    #   FIL/USDT:USDT   is_short=True  open_since=2026-08-28 17:07:13
    #   SAND/USDT:USDT  is_short=True  open_since=2026-08-28 17:07:14
    #   AXS/USDT:USDT   is_short=True  open_since=2026-08-28 17:07:14
    #
    # Three positions, one second, all short, on coins whose average pairwise
    # correlation is 0.62 (research/correlation_results.txt). That is not three
    # bets, it is one bet in three places, opened at the single most crowded
    # moment - and it consumed three of the five same-side slots, after which
    # the account was closed for business while the rest of the month's signals
    # went past.
    #
    # At 1 per candle the account still reaches five per side, but it needs at
    # least five hours to get there and the five come from five different market
    # moments. Nominal diversification becomes real diversification.
    #
    # IT DOES NOT MAKE THE STRATEGY PROFITABLE. -12% is not a business. It is a
    # genuine improvement to a strategy that still loses - see
    # docs/findings/07-why-the-hourly-bot-loses.md before reading anything more
    # into it.
    #
    # Compared against the candle boundary rather than a rolling hour so that
    # backtest and live agree: in backtesting current_time IS the candle start,
    # while live it is a few seconds past it.
    max_new_per_candle = int(os.environ.get("FT_MAX_NEW", "1"))

    @property
    def protections(self):
        # Hourly candles, so these windows are in HOURS not days.
        return [
            {"method": "CooldownPeriod", "stop_duration_candles": 2},
            {
                "method": "MaxDrawdown",
                "lookback_period_candles": 168,      # one week of hours
                "trade_limit": 10,
                "stop_duration_candles": 24,
                "max_allowed_drawdown": 0.15,
            },
            {
                "method": "StoplossGuard",
                "lookback_period_candles": 24,
                "trade_limit": 6,
                "stop_duration_candles": 6,
                "only_per_pair": False,
            },
        ]

    # ----------------------------------------------------------------------
    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        lb = self.breakout_hours.value

        dataframe["atr"] = ta.ATR(dataframe, timeperiod=20)
        dataframe["ema_fast"] = ta.EMA(dataframe, timeperiod=self.ema_fast.value)
        dataframe["ema_slow"] = ta.EMA(dataframe, timeperiod=self.ema_slow.value)
        dataframe["adx"] = ta.ADX(dataframe, timeperiod=14)
        dataframe["rsi"] = ta.RSI(dataframe, timeperiod=14)
        dataframe["vol_sma"] = dataframe["volume"].rolling(20).mean()

        # shift(1) so today's own extreme is not part of the level it must beat
        dataframe["dc_high"] = dataframe["high"].rolling(lb).max().shift(1)
        dataframe["dc_low"] = dataframe["low"].rolling(lb).min().shift(1)

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        base = (
            (dataframe["volume"] > 0)
            & dataframe["atr"].notna()
            & dataframe["dc_high"].notna()
            & dataframe["dc_low"].notna()
            & (dataframe["adx"] > self.adx_floor.value)
            & (dataframe["volume"] > dataframe["vol_sma"])
        )

        dataframe.loc[
            base
            & (dataframe["close"] > dataframe["dc_high"])
            & (dataframe["ema_fast"] > dataframe["ema_slow"])
            & (dataframe["rsi"] < self.rsi_long_max.value),
            ["enter_long", "enter_tag"],
        ] = (1, "h_breakout_up")

        dataframe.loc[
            base
            & (dataframe["close"] < dataframe["dc_low"])
            & (dataframe["ema_fast"] < dataframe["ema_slow"])
            & (dataframe["rsi"] > self.rsi_short_min.value),
            ["enter_short", "enter_tag"],
        ] = (1, "h_breakout_down")

        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        return dataframe

    # ----------------------------------------------------------------------
    def _atr_at(self, pair: str, trade: Trade | None = None) -> float | None:
        dataframe, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
        if dataframe is None or dataframe.empty:
            return None
        row = dataframe.iloc[-1]
        if trade is not None:
            candles = dataframe.loc[dataframe["date"] <= trade.open_date_utc]
            if not candles.empty:
                row = candles.iloc[-1]
        atr = row["atr"]
        if atr is None or atr != atr or atr <= 0:
            return None
        return float(atr)

    def custom_stoploss(
        self, pair: str, trade: Trade, current_time: datetime, current_rate: float,
        current_profit: float, after_fill: bool, **kwargs,
    ) -> float | None:
        entry_atr = self._atr_at(pair, trade)
        if entry_atr is None:
            return None

        initial_dist = entry_atr * self.initial_stop_atr.value
        trail_dist = entry_atr * self.trail_atr.value

        if trade.is_short:
            best = trade.min_rate or trade.open_rate
            stop_price = min(best + trail_dist, trade.open_rate + initial_dist)
        else:
            best = trade.max_rate or trade.open_rate
            stop_price = max(best - trail_dist, trade.open_rate - initial_dist)

        # keep the stop inside liquidation, or the exchange closes us first
        liq = trade.liquidation_price
        if liq:
            if trade.is_short:
                stop_price = min(stop_price, float(liq) * 0.98)
            else:
                stop_price = max(stop_price, float(liq) * 1.02)

        return stoploss_from_absolute(
            stop_price, current_rate=current_rate,
            is_short=trade.is_short, leverage=trade.leverage,
        )

    def custom_stake_amount(
        self, pair: str, current_time: datetime, current_rate: float,
        proposed_stake: float, min_stake: float | None, max_stake: float,
        leverage: float, entry_tag: str | None, side: str, **kwargs,
    ) -> float:
        atr = self._atr_at(pair)
        if atr is None or current_rate <= 0:
            return proposed_stake

        stop_distance_pct = (atr * self.initial_stop_atr.value) / current_rate
        if stop_distance_pct <= 0:
            return proposed_stake

        equity = self.wallets.get_total_stake_amount()
        stake = (equity * self.risk_per_trade.value) / (stop_distance_pct * max(leverage, 1.0))
        stake = min(stake, max_stake)

        if min_stake and stake < min_stake:
            forced_risk = min_stake * max(leverage, 1.0) * stop_distance_pct
            if equity > 0 and (forced_risk / equity) > self.max_forced_risk:
                return 0.0
            stake = min_stake

        return float(stake)

    def confirm_trade_entry(
        self, pair: str, order_type: str, amount: float, rate: float,
        time_in_force: str, current_time: datetime, entry_tag: str | None,
        side: str, **kwargs,
    ) -> bool:
        if self.max_same_side <= 0 and self.max_new_per_candle <= 0:
            return True
        try:
            open_trades = Trade.get_open_trades()
        except Exception:
            return True

        if self.max_same_side > 0:
            want_short = side == "short"
            held = sum(1 for t in open_trades if bool(t.is_short) == want_short)
            if held >= self.max_same_side:
                return False

        if self.max_new_per_candle > 0:
            candle_start = current_time.replace(minute=0, second=0, microsecond=0)
            opened_now = sum(1 for t in open_trades
                             if t.open_date_utc and t.open_date_utc >= candle_start)
            if opened_now >= self.max_new_per_candle:
                return False

        return True

    def leverage(
        self, pair: str, current_time: datetime, current_rate: float,
        proposed_leverage: float, max_leverage: float, entry_tag: str | None,
        side: str, **kwargs,
    ) -> float:
        if self.force_leverage > 0:
            return float(max(1.0, min(self.force_leverage, max_leverage)))

        atr = self._atr_at(pair)
        if atr is None or current_rate <= 0:
            return min(2.0, max_leverage)

        stop_distance_pct = (atr * self.initial_stop_atr.value) / current_rate
        if stop_distance_pct <= 0:
            return min(2.0, max_leverage)

        liq_capped = 1.0 / (stop_distance_pct * self.liq_safety_factor)
        return float(max(1.0, min(liq_capped, self.hard_leverage_cap, max_leverage)))
