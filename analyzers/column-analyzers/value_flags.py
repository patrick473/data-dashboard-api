import pandas as pd


def analyze_value_flags(series: pd.Series, dtype: str) -> dict:
    if dtype != "numeric":
        return {}

    numeric = pd.to_numeric(series, errors="coerce").dropna()
    if numeric.empty:
        return {}

    return {
        "negative_count": int((numeric < 0).sum()),
        "zero_count": int((numeric == 0).sum()),
    }
