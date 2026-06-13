from pathlib import Path

import pandas as pd


def analyze_file_metadata(df: pd.DataFrame, file_path: Path) -> dict:
    return {
        "file": {
            "name": file_path.name,
            "size_bytes": file_path.stat().st_size,
        }
    }
