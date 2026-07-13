import pandas as pd
from src.bot.strategies.etf_rotation import ETFRotationStrategy

prices = pd.read_parquet("data/prices.parquet")
prices["date"] = pd.to_datetime(prices["date"])

strategy = ETFRotationStrategy()
asof = prices["date"].max()
weights = strategy.target_weights(prices, asof)

print("Decision date:", asof.date())
print("Target picks:", weights)