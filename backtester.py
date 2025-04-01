import vectorbt as vbt
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path
from base import StrategyBase


class Backtester:
    def __init__(self, data: dict, output_dir: str = "results"):
        self.data = data  # {pair: DataFrame}
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def run(self, strategy: StrategyBase, pair: str):
        strategy_instance = strategy(self.data[pair])
        signals = strategy_instance.generate_signals()
        equity = strategy_instance.run_backtest()

        # Збереження графіку
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=equity.index, y=equity,
                      mode="lines", name="Equity"))
        fig.write_image(self.output_dir / f"{pair}_equity.png")

        # Метрики
        metrics = strategy_instance.get_metrics()
        return metrics

    def run_all(self, strategy: StrategyBase) -> pd.DataFrame:
        results = {pair: self.run(strategy, pair) for pair in self.data.keys()}
        return pd.DataFrame(results).T
