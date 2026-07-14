import os
from dotenv import load_dotenv
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

load_dotenv()  # read keys from the .env file

KEY = (os.getenv("APCA_API_KEY_ID") or "").strip()
SECRET = (os.getenv("APCA_API_SECRET_KEY") or "").strip()
DRY_RUN = os.getenv("DRY_RUN", "true").lower() == "true"

# paper=True guarantees we NEVER touch a live account
client = TradingClient(KEY, SECRET, paper=True)

def get_equity():
    return float(client.get_account().equity)

def submit_target_orders(weights):
    equity = get_equity()
    for symbol, weight in weights.items():
        notional = round(equity * weight, 2)   # dollars to allocate
        order = MarketOrderRequest(
            symbol=symbol,
            notional=notional,
            side=OrderSide.BUY,
            time_in_force=TimeInForce.DAY,
        )
        if DRY_RUN:
            print(f"DRY RUN -> BUY {symbol} ${notional}")
        else:
            client.submit_order(order_data=order)
            print(f"SUBMITTED -> BUY {symbol} ${notional}")