import pandas as pd


def analyze_gap_stats(series: pd.Series, dtype: str) -> dict:
    if dtype != "datetime":
        return {}

    parsed = pd.to_datetime(series, errors="coerce").dropna().sort_values()
    if len(parsed) < 2:
        return {}

    gaps = parsed.diff().dropna().dt.total_seconds()

    return {
        "gap_stats": {
            "min_seconds": round(float(gaps.min()), 3),
            "max_seconds": round(float(gaps.max()), 3),
            "mean_seconds": round(float(gaps.mean()), 3),
            "median_seconds": round(float(gaps.median()), 3),
        }
    }
