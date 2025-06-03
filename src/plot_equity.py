import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio

pio.renderers.default = 'browser'

def plot_equity_curve(csv_path='data/equity_curve.csv', title='Strategy Equity Curve'):
    df = pd.read_csv(csv_path)

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        y=df['equity'],
        mode='lines',
        line=dict(color='deepskyblue', width=3),
        name='Equity'
    ))

    fig.update_layout(
        title=title,
        xaxis_title='Trade Number',
        yaxis_title='Equity ($)',
        template='plotly_dark',
        font=dict(family='Courier New', size=14),
        height=600,
        width=1000,
        plot_bgcolor='black',
        paper_bgcolor='black',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='gray')
    )

    fig.show()

if __name__ == "__main__":
    plot_equity_curve()