import importlib
import logging
from pathlib import Path

import pandas as pd

from .utils import infer_dtype

_ca = importlib.import_module(".column-analyzers", package=__package__)
COLUMN_ANALYZERS = _ca.COLUMN_ANALYZERS


def analyze_columns(df: pd.DataFrame, file_path: Path) -> dict:
    columns = []
    total_cols = len(df.columns)
    for i, col_name in enumerate(df.columns, start=1):
        logging.info("  Column %d/%d — %s", i, total_cols, col_name)
        series = df[col_name]
        dtype = infer_dtype(series)

        col_meta: dict = {"name": col_name, "dtype": dtype}
        for analyzer in COLUMN_ANALYZERS:
            logging.info("    Running analyzer: %s", analyzer.__name__)
            col_meta.update(analyzer(series, dtype))

        columns.append(col_meta)

    return {"columns": columns}
