from pathlib import Path

class RiskEngine:
    def __init__(self, config):
        self.config = config

    def check_kill_switch(self):
        # If the KILL_SWITCH file exists, stop everything immediately
        if Path(self.config["kill_switch_file"]).exists():
            raise RuntimeError("KILL SWITCH ACTIVE - no orders will be sent")

    def check_order(self, symbol, notional):
        # Block orders that are too big or for symbols not on the allowed list
        if notional > self.config["max_order_notional"]:
            raise ValueError(f"{symbol}: order too big ({notional})")
        if symbol not in self.config["allowed_symbols"]:
            raise ValueError(f"{symbol}: not on the allowed list")

    def check_portfolio(self, weights):
        gross = sum(abs(w) for w in weights.values())
        if gross > self.config["max_gross_exposure"]:
            raise ValueError("Total exposure too high")
        for symbol, w in weights.items():
            if abs(w) > self.config["max_symbol_weight"]:
                raise ValueError(f"{symbol}: single position too large")