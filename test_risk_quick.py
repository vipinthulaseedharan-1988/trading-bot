from src.bot.risk.checks import RiskEngine

config = {
    "kill_switch_file": "./KILL_SWITCH",
    "max_order_notional": 1000,
    "max_gross_exposure": 1.0,
    "max_symbol_weight": 0.50,
    "allowed_symbols": ["SPY", "QQQ", "IWM", "TLT", "GLD", "SHY"],
}
risk = RiskEngine(config)
# 1. Kill switch check (should pass - no KILL_SWITCH file yet)
risk.check_kill_switch()
print("✅ Kill switch check passed (no kill switch active)")

# 2. A safe portfolio (should pass)
risk.check_portfolio({"QQQ": 0.5, "IWM": 0.5})
print("✅ Safe portfolio passed")

# 3. A dangerous order (should be BLOCKED)
try:
    risk.check_order("QQQ", 5000)   # too big!
except ValueError as e:
    print("🛡️ Blocked as expected:", e)
# 4. An unapproved symbol (should be BLOCKED)
try:
    risk.check_order("TSLA", 500)   # not on allowed list!
except ValueError as e:
    print("🛡️ Blocked as expected:", e)