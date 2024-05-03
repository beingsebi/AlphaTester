"""
File for constants
"""

from enum import Enum


class DbConstants:
    """
    Constants for database connection
    """

    DB_PARAMS = {
        "database": "alphatester",
        "user": "postgres",
        "host": "localhost",
        "password": "123456",
        "port": 5432,
    }


class Timeframe(Enum):
    M1 = "1m"
    M5 = "5m"
    M15 = "15m"
    M30 = "30m"
    H1 = "1h"
    H4 = "4h"
    D1 = "1d"
    W1 = "1w"
    MN1 = "1M"


class Sources(Enum):
    CLOSE = "close"
    OPEN = "open"
    HIGH = "high"
    LOW = "low"


class IndicatorNames(Enum):
    SMA = "sma"
    EMA = "ema"
    RSI = "rsi"
    MACD = "macd"
