import pandas as pd


def infer_dtype(series: pd.Series) -> str:
    """Map a pandas Series to one of the frontend dtype labels."""
    if pd.api.types.is_bool_dtype(series):
        return "boolean"
    if pd.api.types.is_numeric_dtype(series):
        return "numeric"
    if pd.api.types.is_datetime64_any_dtype(series):
        return "datetime"
    if series.dtype.name == "category":
        return "categorical"
    if series.dtype == object:
        sample = series.dropna().head(20)
        try:
            pd.to_datetime(sample)
            return "datetime"
        except (ValueError, TypeError):
            pass
        if series.nunique() <= 20 and series.nunique() / max(len(series), 1) < 0.1:
            return "categorical"
    return "string"


def safe_float(value) -> float | None:
    try:
        result = float(value)
        return None if pd.isna(result) else result
    except (TypeError, ValueError):
        return None
