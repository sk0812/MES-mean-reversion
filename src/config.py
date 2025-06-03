"""
Trading system configuration parameters.
"""
from dataclasses import dataclass
from typing import Dict

@dataclass
class VWAPConfig:
    window: int = 30
    zscore_threshold: float = 2.0
    zscore_smooth_span: int = 5
    throttle_bars: int = 10

@dataclass
class IBKRConfig:
    host: str = "127.0.0.1"
    port: int = 7497
    client_id: int = 3

@dataclass
class TradingConfig:
    symbol: str = "MES"
    exchange: str = "CME"
    duration: str = "1 D"
    bar_size: str = "1 min"
    use_rth: bool = False

# Default configurations
DEFAULT_VWAP_CONFIG = VWAPConfig()
DEFAULT_IBKR_CONFIG = IBKRConfig()
DEFAULT_TRADING_CONFIG = TradingConfig() 