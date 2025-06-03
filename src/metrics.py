import pandas as pd
import numpy as np

def evaluate_performance(trades_df: pd.DataFrame, risk_free_rate: float = 0.0):
    if trades_df.empty:
        print("No trades executed.")
        return

    n = len(trades_df)
    wins = trades_df[trades_df['pnl'] > 0]
    losses = trades_df[trades_df['pnl'] <= 0]

    total_pnl = trades_df['pnl'].sum()
    avg_pnl = trades_df['pnl'].mean()
    win_rate = len(wins) / n * 100
    pnl_std = trades_df['pnl'].std()

    # Sharpe Ratio (scaled by sqrt(n))
    sharpe = (avg_pnl - risk_free_rate) / pnl_std * np.sqrt(n) if pnl_std > 0 else np.nan

    # Max Drawdown (on points equity curve)
    cumulative_pnl = trades_df['pnl'].cumsum()
    running_max = cumulative_pnl.cummax()
    drawdown = cumulative_pnl - running_max
    max_drawdown = drawdown.min()

    # Profit Factor
    gross_profit = wins['pnl'].sum()
    gross_loss = losses['pnl'].sum()
    profit_factor = gross_profit / abs(gross_loss) if gross_loss != 0 else np.inf

    # Expectancy
    expectancy = avg_pnl

    # Avg win/loss
    avg_win = wins['pnl'].mean() if not wins.empty else 0
    avg_loss = losses['pnl'].mean() if not losses.empty else 0

    print(f"\n📊 Performance Metrics:")
    print(f"---------------------------")
    print(f"Total Trades:        {n}")
    print(f"Win Rate:            {win_rate:.2f}%")
    print(f"Total PnL:           {total_pnl:.2f} points")
    print(f"Average PnL/Trade:   {avg_pnl:.2f} points")
    print(f"Sharpe Ratio:        {sharpe:.2f}")
    print(f"Max Drawdown:        {max_drawdown:.2f} points")
    print(f"Profit Factor:       {profit_factor:.2f}")
    print(f"Expectancy:          {expectancy:.2f} points/trade")
    print(f"Avg Win / Avg Loss:  {avg_win:.2f} / {avg_loss:.2f}")