import pandas as pd

from ..utils import safe_float


def analyze_numeric(series: pd.Series, dtype: str) -> dict:
    if dtype != "numeric":
        return {}
    return {
        "min": safe_float(series.min()),
        "max": safe_float(series.max()),
        "mean": safe_float(series.mean()),
        "std": safe_float(series.std()),
        "median": safe_float(series.median()),
    }
