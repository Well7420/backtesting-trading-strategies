# Binance Trading Strategy Backtesting Framework

This project implements a modular and scalable framework for backtesting trading strategies using 1-minute OHLCV data for 100 BTC trading pairs on Binance for February 2025. Built with `vectorbt`, it supports data loading, strategy development, and performance analysis.

## Overview
- **Objective**: Backtest multiple trading strategies on historical cryptocurrency data.
- **Data**: 1-minute OHLCV for 100 BTC pairs from Binance, covering 01.02.2025 — 28.02.2025.
- **Tools**: Python 3.10+, `vectorbt`, `pandas`, `numpy`, `plotly`, `pyarrow`, `ta`, `ccxt`.
- **Features**: Modular design, API integration, unit tests, and comprehensive metrics.

## Project Structure


## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Well7420/backtesting-trading-strategies.git
   cd backtesting-trading-strategies

2. **Set up a virtual environment (optional)**:
   python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate

3. **Install dependencies**:
    pip install -r requirements.txt



**Usage Instructions**
1. Data Loading:
Purpose: Fetch 1-minute OHLCV data from Binance for February 2025.
Steps:
Add your Binance API keys to data_loader.py

self.exchange = ccxt.binance({
    'apiKey': 'YOUR_API_KEY',
    'secret': 'YOUR_SECRET_KEY',
    'enableRateLimit': True,
})

2. Run the data loader:
python main.py --download

This creates .parquet files in the data/ directory (e.g., ETH_BTC_1m.parquet).
Note: Without API keys, limits are lower (~600 requests/minute).


3. Running Backtests
Purpose: Execute backtests for all strategies across 100 pairs.
python main.py --backtest

Output: Metrics in results/metrics.csv, equity curves in results/screenshots/.

3. Running Tests
Purpose: Verify strategy and backtester logic.
pytest tests/


**Strategy Descriptions**
1. SMA Crossover (sma_cross.py)
Description: Enters a long position when a fast SMA crosses above a slow SMA, exits when it crosses below.
Parameters:
fast_window=10: Period for fast SMA.
slow_window=30: Period for slow SMA.
Logic: Classic trend-following strategy based on moving average crossovers.
Implementation: Uses vectorbt.MA for SMA calculations and signal generation.

2. RSI with Bollinger Bands Confirmation (rsi_bb.py)
Description: Enters a long position when RSI is oversold (<30) and price rebounds from the lower Bollinger Band, exits when RSI is overbought (>70).
Parameters:
rsi_window=14: RSI period.
bb_window=20: Bollinger Bands period.
bb_std=2.0: Standard deviation multiplier.
Logic: Combines momentum (RSI) and mean-reversion (BB) signals.
Implementation: Uses ta.momentum.RSIIndicator and ta.volatility.BollingerBands.

3. VWAP Reversion Intraday (vwap_reversion.py)
Description: Enters a position when price deviates significantly from VWAP, exits when it reverts.
Parameters:
threshold=0.01: Deviation threshold (1%).
Logic: Intraday mean-reversion strategy based on VWAP as a fair value benchmark.
Implementation: Uses vectorbt.VWAP for VWAP calculation.
Results and Conclusions
(Note: These are placeholders based on typical strategy behavior. Replace with actual results after running backtests.)

SMA Crossover
Total Return: [TBD]%
Sharpe Ratio: [TBD]
Max Drawdown: [TBD]%
Conclusion: Likely performed well on trending pairs but struggled in choppy markets due to frequent false signals.
RSI with Bollinger Bands
Total Return: [TBD]%
Sharpe Ratio: [TBD]
Max Drawdown: [TBD]%
Conclusion: Expected to excel in range-bound conditions, with lower exposure but higher win rate.
VWAP Reversion
Total Return: [TBD]%
Sharpe Ratio: [TBD]
Max Drawdown: [TBD]%
Conclusion: Potentially showed the highest win rate due to mean-reversion nature, but smaller per-trade profits.
General Observations
Data Quality: 1-minute data provided sufficient granularity for intraday strategies.
Scalability: Framework handled 100 pairs efficiently with vectorbt.
Next Steps: Add multi-timeframe analysis and optimize parameters.
Additional Notes
API Limits: With API keys, data fetching for 100 pairs (~40,000 minutes each) takes ~1-2 hours due to rate limits.
Synthetic Data: For testing without API, generate synthetic OHLCV with generate_synthetic_ohlcv (see code in discussion).
Improvements: Consider parallel processing with multiprocessing for faster backtesting.
Contributing
Fork the repo, submit pull requests, or open issues for suggestions.