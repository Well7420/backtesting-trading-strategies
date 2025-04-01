import vectorbt as vbt
import pandas as pd
from .base import StrategyBase


class SMACrossStrategy(StrategyBase):
    def __init__(self, price_data: pd.DataFrame, fast_window: int = 10, slow_window: int = 30):
        super().__init__(price_data)
        self.fast_window = fast_window
        self.slow_window = slow_window
        self.signals = None

    def generate_signals(self) -> pd.DataFrame:
        fast_sma = vbt.MA.run(
            self.price_data["close"], window=self.fast_window)
        slow_sma = vbt.MA.run(
            self.price_data["close"], window=self.slow_window)
        entries = fast_sma.ma_crossed_above(slow_sma)
        exits = fast_sma.ma_crossed_below(slow_sma)
        self.signals = pd.DataFrame({
            "entries": entries.astype(int),
            "exits": exits.astype(int)
        })
        return self.signals

    def run_backtest(self) -> pd.DataFrame:
        if self.signals is None:
            self.generate_signals()
        pf = vbt.Portfolio.from_signals(
            self.price_data["close"],
            entries=self.signals["entries"],
            exits=self.signals["exits"],
            fees=self.commission,
            slippage=self.slippage
        )
        return pf.total_profit()

    def get_metrics(self) -> dict:
        pf = vbt.Portfolio.from_signals(
            self.price_data["close"],
            entries=self.signals["entries"],
            exits=self.signals["exits"],
            fees=self.commission,
            slippage=self.slippage
        )
        return {
            "total_return": pf.total_return(),
            "sharpe_ratio": pf.sharpe_ratio(),
            "max_drawdown": pf.max_drawdown()
        }
