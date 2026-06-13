import logging
from pathlib import Path

import pandas as pd

from .utils import infer_dtype, safe_float


def analyze_columns(df: pd.DataFrame, file_path: Path) -> dict:
    columns = []
    total_cols = len(df.columns)
    for i, col_name in enumerate(df.columns, start=1):
        logging.info("  Column %d/%d — %s", i, total_cols, col_name)
        series = df[col_name]
        dtype = infer_dtype(series)

        null_count = int(series.isna().sum())
        col_meta: dict = {
            "name": col_name,
            "dtype": dtype,
            "null_count": null_count,
            "fill_rate": round((len(series) - null_count) / len(series), 4) if len(series) > 0 else 0.0,
            "unique_count": int(series.nunique()),
            "top_values": [str(v) for v in series.dropna().value_counts().head(5).index],
        }

        if dtype == "numeric":
            col_meta["min"] = safe_float(series.min())
            col_meta["max"] = safe_float(series.max())
            col_meta["mean"] = safe_float(series.mean())
            col_meta["std"] = safe_float(series.std())
            col_meta["median"] = safe_float(series.median())
        elif dtype == "datetime":
            parsed = pd.to_datetime(series, errors="coerce")
            col_meta["min"] = str(parsed.min()) if not pd.isna(parsed.min()) else None
            col_meta["max"] = str(parsed.max()) if not pd.isna(parsed.max()) else None

        columns.append(col_meta)

    return {"columns": columns}
