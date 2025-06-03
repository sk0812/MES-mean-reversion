"""
Main script for connecting to Interactive Brokers and running the trading strategy.
"""
from ib_insync import *
from src.plot import plot_candles_with_vwap
from src.signals import compute_vwap_zscore_signals
from src.backtest import simulate_trades
from src.metrics import evaluate_performance
from src.config import DEFAULT_IBKR_CONFIG, DEFAULT_TRADING_CONFIG, DEFAULT_VWAP_CONFIG

def main():
    # Initialize connection
    ib = IB()
    ib.connect(
        DEFAULT_IBKR_CONFIG.host,
        DEFAULT_IBKR_CONFIG.port,
        clientId=DEFAULT_IBKR_CONFIG.client_id
    )

    try:
        # Get contract details
        contracts = ib.reqContractDetails(
            Future(
                symbol=DEFAULT_TRADING_CONFIG.symbol,
                exchange=DEFAULT_TRADING_CONFIG.exchange
            )
        )
        contract = contracts[0].contract

        # Request historical data
        bars = ib.reqHistoricalData(
            contract,
            endDateTime='',
            durationStr=DEFAULT_TRADING_CONFIG.duration,
            barSizeSetting=DEFAULT_TRADING_CONFIG.bar_size,
            whatToShow='TRADES',
            useRTH=DEFAULT_TRADING_CONFIG.use_rth,
            formatDate=1
        )

        # Process data and generate signals
        df = util.df(bars)
        df = compute_vwap_zscore_signals(df, config=DEFAULT_VWAP_CONFIG)

        # Simulate trades and evaluate
        trades_df = simulate_trades(df, cooldown_bars=DEFAULT_VWAP_CONFIG.throttle_bars)
        evaluate_performance(trades_df)

        # Plot results
        plot_candles_with_vwap(df, trades_df)

    finally:
        ib.disconnect()

if __name__ == "__main__":
    main()