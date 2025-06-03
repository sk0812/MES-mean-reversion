import pandas as pd

def simulate_trades(df: pd.DataFrame, equity_start: float = 5000, risk_pct: float = 0.01, multiplier: float = 5, cooldown_bars: int = 10, max_contracts=5):
    df = df.copy()

    # ATR calculation (true range)
    df['prev_close'] = df['close'].shift(1)
    df['tr'] = df[['high', 'prev_close']].max(axis=1) - df[['low', 'prev_close']].min(axis=1)
    df['atr'] = df['tr'].rolling(14).mean()
    df = df.dropna(subset=['atr'])

    commission_per_contract = 1.25  # USD per round-trip
    slippage_per_contract = 0.15    # in points

    trades = []
    position = None
    cooldown = 0
    equity = equity_start

    for i in range(len(df) - 1):
        row = df.iloc[i]
        next_row = df.iloc[i + 1]

        if position is None and cooldown == 0:
            risk_per_trade = equity * risk_pct
            atr = row['atr']
            point_risk = max(atr * 0.8, 0.5)
            usd_risk_per_contract = point_risk * multiplier

            if point_risk <= 0 or not pd.notna(point_risk):
                continue

            contracts = min(int(risk_per_trade // usd_risk_per_contract), max_contracts)
            if contracts == 0:
                continue

            if row['long_signal']:
                position = {
                    'type': 'long',
                    'entry_time': row['date'],
                    'entry_price': row['close'],
                    'sl': row['close'] - point_risk,
                    'tp': row['close'] + atr * 2.4,
                    'contracts': contracts
                }
            elif row['short_signal']:
                position = {
                    'type': 'short',
                    'entry_time': row['date'],
                    'entry_price': row['close'],
                    'sl': row['close'] + point_risk,
                    'tp': row['close'] - atr * 2.4,
                    'contracts': contracts
                }

        elif position:
            high = next_row['high']
            low = next_row['low']
            contracts = position['contracts']

            if position['type'] == 'long':
                if low <= position['sl']:
                    exit_price = position['sl']
                    result = 'stop_loss'
                elif high >= position['tp']:
                    exit_price = position['tp']
                    result = 'take_profit'
                else:
                    continue
                pnl_points = exit_price - position['entry_price']

            elif position['type'] == 'short':
                if high >= position['sl']:
                    exit_price = position['sl']
                    result = 'stop_loss'
                elif low <= position['tp']:
                    exit_price = position['tp']
                    result = 'take_profit'
                else:
                    continue
                pnl_points = position['entry_price'] - exit_price

            commission_points = commission_per_contract / multiplier
            pnl_net = pnl_points - (slippage_per_contract + commission_points) * contracts
            pnl_usd = pnl_net * contracts * multiplier
            equity += pnl_usd
            trades.append({
                'type': position['type'],
                'entry_time': position['entry_time'],
                'entry_price': position['entry_price'],
                'exit_time': next_row['date'],
                'exit_price': exit_price,
                'contracts': contracts,
                'pnl': pnl_net,
                'pnl_usd': pnl_usd,
                'result': result,
                'equity_after': equity
            })
            position = None
            cooldown = cooldown_bars

        else:
            cooldown = max(0, cooldown - 1)

    return pd.DataFrame(trades)