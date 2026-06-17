import pandas as pd


DEFAULT_TOP_N = 20


def analyze_frequency(series: pd.Series, dtype: str) -> dict:
    if dtype not in ("categorical", "string"):
        return {}

    counts = series.dropna().value_counts()
    total = int(counts.sum())

    return {
        "frequency": [
            {
                "value": str(value),
                "count": int(count),
                "rate": round(int(count) / total, 4) if total > 0 else 0.0,
            }
            for value, count in counts.head(DEFAULT_TOP_N).items()
        ]
    }
