import os
from dotenv import load_dotenv
from alpaca.trading.client import TradingClient

load_dotenv()
client = TradingClient(
    os.getenv("APCA_API_KEY_ID"),
    os.getenv("APCA_API_SECRET_KEY"),
    paper=True,
)
acct = client.get_account()
print("✅ Connected! Paper cash balance: $", acct.cash)
print("Account status:", acct.status)