import pandas as pd
import matplotlib.pyplot as plt

def plot_day_trades(df: pd.DataFrame, trades: pd.DataFrame, day: str):
    """
    Plots trades on a price chart for a single day.

    Args:
        df (pd.DataFrame): Original OHLCV + signals data.
        trades (pd.DataFrame): Trades log from simulate_trades.
        day (str): Date string in 'YYYYMMDD' format (e.g., '20250417').
    """

    # Filter data
    df_day = df[df['date'].dt.strftime('%Y%m%d') == day].copy()
    trades_day = trades[trades['entry_time'].dt.strftime('%Y%m%d') == day]

    if df_day.empty or trades_day.empty:
        print(f"No trades or data found for {day}")
        return

    plt.figure(figsize=(14, 6))
    plt.plot(df_day['date'], df_day['close'], label='Close Price', color='black', linewidth=1)

    for _, trade in trades_day.iterrows():
        entry_idx = df_day[df_day['date'] == trade['entry_time']].index
        exit_idx = df_day[df_day['date'] == trade['exit_time']].index
        if entry_idx.empty or exit_idx.empty:
            continue

        # Entry marker
        plt.scatter(trade['entry_time'], trade['entry_price'], 
                    color='green' if trade['type'] == 'long' else 'red', 
                    marker='^' if trade['type'] == 'long' else 'v', 
                    label='Entry' if _ == trades_day.index[0] else "", s=60)

        # Exit marker
        plt.scatter(trade['exit_time'], trade['exit_price'], 
                    color='blue' if trade['result'] == 'take_profit' else 'orange', 
                    marker='x', 
                    label='Exit (TP/SL)' if _ == trades_day.index[0] else "", s=60)

        # Draw SL/TP lines
        plt.plot([trade['entry_time'], trade['exit_time']], 
                 [trade['entry_price'], trade['exit_price']], 
                 linestyle='--', alpha=0.5, color='gray')

    plt.title(f"Trades on {day}")
    plt.xlabel("Time")
    plt.ylabel("Price")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()