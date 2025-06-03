import pandas as pd
import os
from signals import compute_vwap_zscore_signals
from backtest import simulate_trades
from metrics import evaluate_performance
from plot_trades import plot_day_trades

DATA_PATH = "data/"
files = sorted([f for f in os.listdir(DATA_PATH) if f.endswith(".csv")])

all_trades = []
equity_curve = []

# Initialize equity
equity = 5000

for file in files:
    df = pd.read_csv(os.path.join(DATA_PATH, file), parse_dates=['date'])
    df = compute_vwap_zscore_signals(df)

    # Simulate trades with current equity
    trades = simulate_trades(df, equity_start=equity)

    if not trades.empty:
        trades["day"] = file.split("_")[1].split(".")[0]
        all_trades.append(trades)

        equity += trades["pnl"].sum()  # Use pnl in points
        equity_curve.extend(trades["equity_after"].tolist())  # Still in points

# Combine all trades
all_trades_df = pd.concat(all_trades, ignore_index=True)

# Save logs
all_trades_df.to_csv("data/full_trade_log.csv", index=False)
pd.DataFrame({'equity': equity_curve}).to_csv("data/equity_curve.csv", index=False)

# Output
print(all_trades_df)
evaluate_performance(all_trades_df)

# Plotting section
day_to_plot = "20250417"
df = pd.read_csv(f"data/MES_{day_to_plot}.csv", parse_dates=['date'])
df = compute_vwap_zscore_signals(df)

# Ensure datetime format
all_trades_df['entry_time'] = pd.to_datetime(all_trades_df['entry_time'], utc=True).dt.tz_localize(None)
all_trades_df['exit_time'] = pd.to_datetime(all_trades_df['exit_time'], utc=True).dt.tz_localize(None)

# Visualise
plot_day_trades(df, all_trades_df, day_to_plot)