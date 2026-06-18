import pandas as pd


DEFAULT_BIN_COUNT = 20


def _remove_outliers(numeric: pd.Series) -> pd.Series:
    q1 = numeric.quantile(0.25)
    q3 = numeric.quantile(0.75)
    iqr = q3 - q1
    lower_fence = q1 - 1.5 * iqr
    upper_fence = q3 + 1.5 * iqr
    return numeric[(numeric >= lower_fence) & (numeric <= upper_fence)]


def analyze_distribution(series: pd.Series, dtype: str) -> dict:
    if dtype != "numeric":
        return {}

    numeric = pd.to_numeric(series, errors="coerce").dropna()
    if numeric.empty:
        return {"distribution": []}

    numeric = _remove_outliers(numeric)
    if numeric.empty:
        return {"distribution": []}

    min_val = float(numeric.min())
    max_val = float(numeric.max())

    if min_val == max_val:
        return {"distribution": [{"min": min_val, "max": max_val, "count": int(numeric.count())}]}

    counts, bin_edges = pd.cut(numeric, bins=DEFAULT_BIN_COUNT, retbins=True, right=True)

    distribution = [
        {
            "min": round(float(bin_edges[i]), 6),
            "max": round(float(bin_edges[i + 1]), 6),
            "count": int((counts == counts.cat.categories[i]).sum()),
        }
        for i in range(len(counts.cat.categories))
    ]

    return {"distribution": distribution}
