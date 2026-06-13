# How to add a new analyzer

Each analyzer is a plain Python function with this signature:

```python
def analyze_something(df: pd.DataFrame, file_path: Path) -> dict:
    ...
```

Its return value is **merged** into the final JSON output, so the key(s) you return become top-level fields in the result file.

---

## Steps

### 1. Create a new file in `analyzers/`

For example, `analyzers/row_stats.py`:

```python
from pathlib import Path
import pandas as pd


def analyze_row_stats(df: pd.DataFrame, file_path: Path) -> dict:
    return {
        "row_stats": {
            "duplicate_count": int(df.duplicated().sum()),
            "fully_empty_rows": int(df.isna().all(axis=1).sum()),
        }
    }
```

### 2. Register it in `__init__.py`

Import your function and append it to the `ANALYZERS` list:

```python
from .row_stats import analyze_row_stats

ANALYZERS: list[Callable[[pd.DataFrame, Path], dict]] = [
    analyze_file_metadata,
    analyze_columns,
    analyze_row_stats,  # <-- add here
]
```

That's it. The pipeline in `analyzeCsvFile.py` calls every function in `ANALYZERS` and merges all results automatically.

---

## Shared helpers

`analyzers/utils.py` provides two reusable helpers:

| Helper | Purpose |
|---|---|
| `infer_dtype(series)` | Maps a pandas Series to `numeric`, `boolean`, `datetime`, `categorical`, or `string` |
| `safe_float(value)` | Converts a value to `float`, returning `None` for NaN/errors |

Import them with:

```python
from .utils import infer_dtype, safe_float
```
