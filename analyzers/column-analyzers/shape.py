import pandas as pd


def analyze_shape(series: pd.Series, dtype: str) -> dict:
    if dtype != "numeric":
        return {}

    numeric = pd.to_numeric(series, errors="coerce").dropna()
    if len(numeric) < 3:
        return {}

    return {
        "skewness": round(float(numeric.skew()), 4),
        "kurtosis": round(float(numeric.kurtosis()), 4),
    }
