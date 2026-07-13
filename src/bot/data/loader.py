import yfinance as yf
import pandas as pd

UNIVERSE = ["SPY", "QQQ", "IWM", "TLT", "GLD", "SHY"]

def download_prices(start="2015-01-01"):
    # Download daily, split/dividend-adjusted prices for all ETFs
    raw = yf.download(UNIVERSE, start=start, auto_adjust=True)["Close"]
    # Reshape into tidy long format: one row per (date, symbol)
    df = raw.stack().rename("close").reset_index()
    df.columns = ["date", "symbol", "close"]
    df = df.sort_values(["symbol", "date"]).reset_index(drop=True)
    df.to_parquet("data/prices.parquet")   # save for later use
    return df

if __name__ == "__main__":
    data = download_prices()
    print("Downloaded rows:", len(data))
    print(data.tail())