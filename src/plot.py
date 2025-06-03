import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio

pio.renderers.default = 'browser'

def plot_candles_with_vwap(df: pd.DataFrame, trades=None, title='MES Candles + VWAP'):
    df = df.copy()
    df['date'] = pd.to_datetime(df['date'])

    # VWAP calculation
    df['cum_vol'] = df['volume'].cumsum()
    df['cum_pv'] = (df['close'] * df['volume']).cumsum()
    df['vwap'] = df['cum_pv'] / df['cum_vol']

    fig = go.Figure()

    # Candlesticks
    fig.add_trace(go.Candlestick(
        x=df['date'],
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close'],
        name='MES',
        increasing_line_color='limegreen',
        decreasing_line_color='crimson',
        line_width=0.8,
        whiskerwidth=0.3
    ))

    # VWAP Line
    fig.add_trace(go.Scatter(
        x=df['date'],
        y=df['vwap'],
        mode='lines',
        name='VWAP',
        line=dict(color='orange', width=2.5)
    ))

    # Long signal markers (optional)
    if 'long_signal' in df.columns:
        longs = df[df['long_signal']]
        fig.add_trace(go.Scatter(
            x=longs['date'],
            y=longs['low'] * 0.998,
            mode='markers',
            marker=dict(size=9, color='lime', symbol='arrow-up'),
            name='Long Signal'
        ))

    # Short signal markers (optional)
    if 'short_signal' in df.columns:
        shorts = df[df['short_signal']]
        fig.add_trace(go.Scatter(
            x=shorts['date'],
            y=shorts['high'] * 1.002,
            mode='markers',
            marker=dict(size=9, color='red', symbol='arrow-down'),
            name='Short Signal'
        ))

    # Trade entries and exits
    if trades is not None and not trades.empty:
        for _, trade in trades.iterrows():
            # Entry
            entry_color = 'green' if trade['type'] == 'long' else 'red'
            entry_symbol = 'triangle-up' if trade['type'] == 'long' else 'triangle-down'

            fig.add_trace(go.Scatter(
                x=[trade['entry_time']],
                y=[trade['entry_price']],
                mode='markers',
                marker=dict(color=entry_color, symbol=entry_symbol, size=12),
                name=f"{trade['type'].capitalize()} Entry"
            ))

            # Exit
            fig.add_trace(go.Scatter(
                x=[trade['exit_time']],
                y=[trade['exit_price']],
                mode='markers',
                marker=dict(color='white', symbol='x', size=10),
                name="Exit"
            ))

    # Layout
    fig.update_layout(
        title=title,
        template='plotly_dark',
        xaxis_title='Time',
        yaxis_title='Price',
        xaxis_rangeslider_visible=False,
        height=700,
        width=1200,
        font=dict(family='Courier New', size=14),
        plot_bgcolor='black',
        paper_bgcolor='black',
        legend=dict(
            bgcolor='rgba(0,0,0,0)',
            bordercolor='rgba(255,255,255,0.2)',
            borderwidth=1
        )
    )

    fig.update_yaxes(showgrid=True, gridcolor='gray', gridwidth=0.5)
    fig.update_xaxes(showgrid=False)

    fig.show()