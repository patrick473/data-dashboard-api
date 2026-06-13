from pathlib import Path

import pandas as pd

from .utils import infer_dtype, safe_float

def analyze_completeness(df: pd.DataFrame, file_path: Path) -> dict:
    total_rows = len(df)
    total_cells = total_rows * len(df.columns)
    total_nulls = int(df.isna().sum().sum())
    overall_fill_rate = round((total_cells - total_nulls) / total_cells, 4) if total_cells > 0 else 0.0
    fully_complete_cols = int((df.isna().sum() == 0).sum())
    rows_with_any_null = int(df.isna().any(axis=1).sum())

    return {
        "total_rows": total_rows,
        "total_columns": len(df.columns),
        "total_cells": total_cells,
        "total_nulls": total_nulls,
        "overall_fill_rate": overall_fill_rate,
        "fully_complete_columns": fully_complete_cols,
        "rows_with_any_null": rows_with_any_null,
    }

