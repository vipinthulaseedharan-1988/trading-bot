import pandas as pd

class ETFRotationStrategy:
    def __init__(self, lookback=126, trend=200, top_n=2):
        self.lookback = lookback   # ~6 months of trading days for momentum
        self.trend = trend         # ~200-day long-term trend filter
        self.top_n = top_n         # how many ETFs to hold

    def target_weights(self, price_df, asof_date):
        # Keep only data up to the decision date, then pivot to columns per symbol
        close = price_df[price_df["date"] <= asof_date] \
                    .pivot(index="date", columns="symbol", values="close")

        # Need enough history for both the momentum and trend windows
        if len(close) < max(self.lookback, self.trend) + 1:
            return {}

        latest = close.iloc[-1]                              # most recent price
        momentum = latest / close.iloc[-self.lookback] - 1   # 6-month return
        sma = close.tail(self.trend).mean()                  # long-term average

        # Eligible = above trend AND positive momentum (safety improvement)
        eligible = momentum[(latest > sma) & (momentum > 0)].dropna()
        if eligible.empty:
            return {}   # nothing qualifies -> hold cash

        selected = eligible.sort_values(ascending=False).head(self.top_n)
        weight = 1.0 / len(selected)                         # equal weight
        return {symbol: weight for symbol in selected.index}