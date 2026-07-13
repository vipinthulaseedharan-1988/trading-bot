import os, json, datetime
from dotenv import load_dotenv
from src.bot.data.loader import download_prices
from src.bot.strategies.etf_rotation import ETFRotationStrategy
from src.bot.risk.checks import RiskEngine
from src.bot.execution.alpaca_broker import submit_target_orders

load_dotenv()

CONFIG = {
    "kill_switch_file": os.getenv("KILL_SWITCH_FILE", "./KILL_SWITCH"),
    "max_order_notional": float(os.getenv("MAX_ORDER_NOTIONAL", 1000)),
    "max_gross_exposure": float(os.getenv("MAX_GROSS_EXPOSURE", 1.0)),
    "max_symbol_weight": float(os.getenv("MAX_SYMBOL_WEIGHT", 0.50)),
    "allowed_symbols": ["SPY", "QQQ", "IWM", "TLT", "GLD", "SHY"],
}

def run():
    prices = download_prices()
    prices["date"] = __import__("pandas").to_datetime(prices["date"])
    asof = prices["date"].max()
    weights = ETFRotationStrategy().target_weights(prices, asof)

    risk = RiskEngine(CONFIG)
    risk.check_kill_switch()
    risk.check_portfolio(weights)

    submit_target_orders(weights)

    # Write a simple audit log line
    os.makedirs("logs", exist_ok=True)
    with open("logs/audit.jsonl", "a") as f:
        f.write(json.dumps({
            "ts": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "asof": str(asof), "weights": weights}) + "\n")
    print("Done. Target weights:", weights)

if __name__ == "__main__":
    run()