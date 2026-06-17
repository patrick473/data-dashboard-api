import pandas as pd


def analyze_quartiles(series: pd.Series, dtype: str) -> dict:
    if dtype != "numeric":
        return {}

    numeric = pd.to_numeric(series, errors="coerce").dropna()
    if numeric.empty:
        return {}

    q1 = float(numeric.quantile(0.25))
    q3 = float(numeric.quantile(0.75))
    iqr = q3 - q1

    lower_fence = q1 - 1.5 * iqr
    upper_fence = q3 + 1.5 * iqr

    return {
        "q1": round(q1, 6),
        "q3": round(q3, 6),
        "iqr": round(iqr, 6),
        "outlier_count": int(((numeric < lower_fence) | (numeric > upper_fence)).sum()),
    }
