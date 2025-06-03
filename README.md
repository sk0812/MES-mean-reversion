# Futures Trading System

A Python-based futures trading system that implements a VWAP-based mean reversion strategy. The system connects to Interactive Brokers for market data and trade execution.

## Features

- VWAP-based mean reversion strategy with Z-score signals
- Real-time connection to Interactive Brokers
- Historical data backtesting
- Performance metrics calculation
- Trade visualization with candlestick charts

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/futures-trading.git
cd futures-trading
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -e .
```

## Configuration

The system uses configuration classes in `src/config.py` for various parameters:

- `VWAPConfig`: Strategy parameters like window size and Z-score thresholds
- `IBKRConfig`: Interactive Brokers connection settings
- `TradingConfig`: Trading parameters like symbol and timeframe

## Usage

1. Make sure Interactive Brokers TWS or IB Gateway is running
2. Run the main script:
```bash
python connect-ibkr.py
```

## Project Structure

```
futures-trading/
├── data/                # Historical price data
├── src/                 # Source code
│   ├── __init__.py
│   ├── signals.py      # Trading signal generation
│   ├── backtest.py     # Backtesting engine
│   ├── metrics.py      # Performance metrics
│   ├── plot.py         # Visualization functions
│   └── config.py       # Configuration classes
├── scripts/            # Utility scripts
├── requirements.txt    # Python dependencies
├── setup.py           # Package setup
└── README.md          # Documentation
```

## License

MIT License 