# utils/helpers.py
from datetime import datetime
from typing import Any


def format_datetime(dt_string: str, format: str = "%Y-%m-%d %H:%M:%S") -> str:
    try:
        if not dt_string:
            return "N/A"
        dt = datetime.strptime(dt_string, "%Y-%m-%d %H:%M:%S")
        return dt.strftime(format)
    except:
        return dt_string


def format_score(score: int) -> str:
    return f"{score:,}"


def format_time(seconds: float) -> str:
    if seconds is None:
        return "N/A"
    
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes:02d}:{secs:02d}"


def safe_divide(numerator: Any, denominator: Any, default: Any = 0) -> float:
    try:
        if denominator == 0:
            return default
        return float(numerator) / float(denominator)
    except:
        return default


def truncate_string(text: str, max_length: int = 50, suffix: str = "...") -> str:
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix