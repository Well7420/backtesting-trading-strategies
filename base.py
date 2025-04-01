import vectorbt as vbt
import pandas as pd
from base import StrategyBase


class SMACrossStrategy(StrategyBase):
    def __init__(self, price_data: pd.DataFrame, fast_window: int = 10, slow_window: int = 30):
        super().__init__(price_data)
        self.fast_window = fast_window
        self.slow_window = slow_window
        self.signals = None
        self.pf = None  # Зберігатимемо результат бектесту

    def generate_signals(self) -> pd.DataFrame:
        """Генерує сигнали на основі перетину двох SMA."""
        fast_sma = vbt.MA.run(
            self.price_data["close"], window=self.fast_window)
        slow_sma = vbt.MA.run(
            self.price_data["close"], window=self.slow_window)

        # Сигнали входу (1) і виходу (-1)
        entries = fast_sma.ma_crossed_above(slow_sma).astype(bool)
        exits = fast_sma.ma_crossed_below(slow_sma).astype(bool)

        self.signals = pd.DataFrame({
            "entries": entries,
            "exits": exits
        }, index=self.price_data.index)
        return self.signals

    def run_backtest(self) -> pd.DataFrame:
        """Виконує бектест стратегії з урахуванням комісій і сліпейджу."""
        if self.signals is None:
            self.generate_signals()

        self.pf = vbt.Portfolio.from_signals(
            close=self.price_data["close"],
            entries=self.signals["entries"],
            exits=self.signals["exits"],
            fees=self.commission,  # Наприклад, 0.1%
            slippage=self.slippage,  # Наприклад, 0.05%
            freq="1T"  # 1 хвилина
        )
        return self.pf.value()  # Повертає equity curve

    def get_metrics(self) -> dict:
        """Повертає ключові метрики бектесту."""
        if self.pf is None:
            self.run_backtest()

        return {
            "total_return": self.pf.total_return(),
            "sharpe_ratio": self.pf.sharpe_ratio(),
            "max_drawdown": self.pf.max_drawdown(),
            "win_rate": self.pf.win_ratio(),
            "expectancy": self.pf.expectancy(),
            "exposure_time": self.pf.position_coverage()
        }
