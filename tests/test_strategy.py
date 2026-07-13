import pandas as pd
from src.bot.strategies.etf_rotation import ETFRotationStrategy

def test_weights_basic():
    # Build a tiny rising-price dataset for two symbols
    dates = pd.date_range("2020-01-01", periods=260, freq="D")
    rows = []
    for i, d in enumerate(dates):
        rows.append({"date": d, "symbol": "SPY", "close": 100 + i})
        rows.append({"date": d, "symbol": "TLT", "close": 100 + i * 0.5})
    df = pd.DataFrame(rows)

    w = ETFRotationStrategy(top_n=2).target_weights(df, df["date"].max())
    assert len(w) <= 2                        # never more than top_n
    assert abs(sum(w.values()) - 1.0) < 1e-6  # weights add up to 1