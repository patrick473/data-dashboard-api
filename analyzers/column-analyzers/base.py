import pandas as pd


def analyze_base(series: pd.Series, dtype: str) -> dict:
    null_count = int(series.isna().sum())
    return {
        "null_count": null_count,
        "fill_rate": round((len(series) - null_count) / len(series), 4) if len(series) > 0 else 0.0,
        "unique_count": int(series.nunique()),
        "top_values": [str(v) for v in series.dropna().value_counts().head(5).index],
    }
