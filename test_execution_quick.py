from src.bot.execution.alpaca_broker import submit_target_orders, get_equity

print("Paper account equity: $", get_equity())

# Use the same picks your strategy made
weights = {"QQQ": 0.5, "IWM": 0.5}
submit_target_orders(weights)