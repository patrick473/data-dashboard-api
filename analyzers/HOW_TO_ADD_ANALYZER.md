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

### 3. Update the OpenAPI spec

Any new fields your analyzer adds to the output must be reflected in `openapi.yaml` at the root of this repo.

- **New top-level fields** on `AnalysisResult`: add them under `components/schemas/AnalysisResult/properties` (and to `required` if they are always present).
- **New per-column fields** on `ColumnStats`: add them under `components/schemas/ColumnStats/properties`. Mark them optional (omit from `required`) if they only appear for certain `dtype` values.
- **New nested objects**: define a new named schema under `components/schemas/` and reference it with `$ref` instead of inlining the shape.

Example — adding a new optional numeric-only field `entropy`:

```yaml
# in components/schemas/ColumnStats/properties:
entropy:
  type:
    - number
    - "null"
  description: Shannon entropy of the value distribution (numeric columns)
```

Example — adding a new object field that needs its own schema:

```yaml
# new top-level schema
MyStats:
  type: object
  required:
    - foo
    - bar
  properties:
    foo:
      type: integer
    bar:
      type: number

# referenced from AnalysisResult or ColumnStats
my_stats:
  $ref: "#/components/schemas/MyStats"
```

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
