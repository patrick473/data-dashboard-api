import pandas as pd


def analyze_datetime(series: pd.Series, dtype: str) -> dict:
    if dtype != "datetime":
        return {}
    parsed = pd.to_datetime(series, errors="coerce")
    return {
        "min": str(parsed.min()) if not pd.isna(parsed.min()) else None,
        "max": str(parsed.max()) if not pd.isna(parsed.max()) else None,
    }
