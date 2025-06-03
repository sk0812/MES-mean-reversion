"""
Signal generation module for the trading system.
Contains implementations of various trading signals and indicators.
"""
from typing import Tuple
import pandas as pd
import numpy as np
from .config import VWAPConfig

def calculate_vwap(df: pd.DataFrame) -> pd.Series:
    """
    Calculate Volume Weighted Average Price (VWAP) for each day.
    
    Args:
        df: DataFrame with 'close', 'volume', and 'date' columns
        
    Returns:
        Series containing VWAP values
    """
    return df.groupby(df['date'].dt.date).apply(
        lambda x: (x['close'] * x['volume']).cumsum() / x['volume'].cumsum()
    ).reset_index(level=0, drop=True)

def calculate_zscore(series: pd.Series, window: int) -> pd.Series:
    """
    Calculate rolling Z-score for a series.
    
    Args:
        series: Input series to calculate Z-score for
        window: Rolling window size
        
    Returns:
        Series containing Z-score values
    """
    return (
        series - series.rolling(window).mean()
    ) / series.rolling(window).std()

def throttle_signals(
    long_signals: pd.Series,
    short_signals: pd.Series,
    throttle_bars: int
) -> Tuple[pd.Series, pd.Series]:
    """
    Apply throttling to trading signals to prevent overtrading.
    
    Args:
        long_signals: Series of long entry signals
        short_signals: Series of short entry signals
        throttle_bars: Minimum bars between signals
        
    Returns:
        Tuple of throttled (long_signals, short_signals)
    """
    throttled_long = pd.Series(False, index=long_signals.index)
    throttled_short = pd.Series(False, index=short_signals.index)
    
    last_long = -np.inf
    last_short = -np.inf
    
    for i in range(len(long_signals)):
        if long_signals.iloc[i] and (i - last_long >= throttle_bars):
            throttled_long.iloc[i] = True
            last_long = i
        if short_signals.iloc[i] and (i - last_short >= throttle_bars):
            throttled_short.iloc[i] = True
            last_short = i
            
    return throttled_long, throttled_short

def compute_vwap_zscore_signals(
    df: pd.DataFrame,
    config: VWAPConfig = VWAPConfig()
) -> pd.DataFrame:
    """
    Compute trading signals based on VWAP deviation Z-score.
    
    Args:
        df: OHLCV DataFrame with 'date' column
        config: VWAPConfig instance with strategy parameters
        
    Returns:
        DataFrame with added columns for VWAP, Z-score, and signals
    """
    df = df.copy()
    df['date'] = pd.to_datetime(df['date'])
    
    # Calculate VWAP and deviation
    df['vwap'] = calculate_vwap(df)
    df['vwap_diff'] = df['close'] - df['vwap']
    
    # Calculate Z-score and smoothed version
    df['zscore'] = calculate_zscore(df['vwap_diff'], config.window)
    df['zscore_smooth'] = df['zscore'].ewm(span=config.zscore_smooth_span).mean()
    
    # Calculate VWAP slope for trend filter
    df['vwap_slope'] = df['vwap'].diff()
    
    # Generate raw signals
    long_signals = (df['zscore_smooth'] < -config.zscore_threshold) & (df['vwap_slope'] >= 0)
    short_signals = (df['zscore_smooth'] > config.zscore_threshold) & (df['vwap_slope'] <= 0)
    
    # Apply throttling
    df['long_signal'], df['short_signal'] = throttle_signals(
        long_signals, short_signals, config.throttle_bars
    )
    
    # Add combined signal column for convenience
    df['signal'] = 0
    df.loc[df['long_signal'], 'signal'] = 1
    df.loc[df['short_signal'], 'signal'] = -1
    
    # Clean up NaN values from rolling calculations
    return df.dropna(subset=['zscore_smooth'])