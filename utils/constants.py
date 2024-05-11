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
        "user": "server",
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
    CLOSE = "CLOSE"
    OPEN = "OPEN"
    HIGH = "HIGH"
    LOW = "LOW"


class IndicatorNames(Enum):
    SMA = "SMA"
    EMA = "EMA"
    RSI = "RSI"
    MACD = "MACD"


class TypeOfSignal(Enum):
    BUY = "BUY"
    SELL = "SELL"


INDICATORS_CHOICES = [("SMA", "SMA"), ("EMA", "EMA")]

SIGNALS_CHOICES = [
    ("CNF", "CNF"),
    ("DNF", "DNF"),
]

TYPE_OF_SIGNAL_CHOICES = [("BUY", "BUY"), ("SELL", "SELL")]

TYPE_OF_OPERATOR_CHOICES = [(">=", ">="), ("<=", "<=")]

TIMEFRAME_CHOICES = [
    ("1m", "1m"),
    ("5m", "5m"),
    ("15m", "15m"),
    ("30m", "30m"),
    ("1h", "1h"),
    ("4h", "4h"),
    ("1d", "1d"),
    ("1w", "1w"),
    ("1M", "1M"),
]
