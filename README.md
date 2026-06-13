# data-dashboard-api

FastAPI backend that pre-processes CSV files into JSON analytics and serves them over HTTP.

## Tech stack

- **Python** with **FastAPI** (`fastapi[standard]`)
- **pandas** for CSV parsing and analysis
- Virtual environment at `../.venv` (workspace root)

## Architecture

```
input/          ← drop raw .csv files here before running the pipeline
data/           ← output: one .json file per .csv (served by the API)
analyze_csv_file.py   ← offline pipeline script (reads input/, writes data/)
main.py               ← FastAPI app (reads data/ at startup, serves it)
analyzers/            ← pluggable analyzer functions
  __init__.py         ← ANALYZERS registry list
  file_metadata.py    ← file-level stats (name, size, row/col counts)
  columns.py          ← per-column stats (dtype, nulls, uniques, top values, numeric stats)
  utils.py            ← shared helpers: infer_dtype(), safe_float()
  HOW_TO_ADD_ANALYZER.md
```

## Two-step workflow

### Step 1 — pre-process CSVs (offline)

Place `.csv` files in `input/`, then run:

```bash
python analyze_csv_file.py
```

This calls every function in `ANALYZERS`, merges their outputs, and writes `data/<stem>.json`.

### Step 2 — serve the API

```bash
fastapi dev          # development (auto-reload)
# or
fastapi run          # production
```

On startup, the app loads every `.json` from `data/` into an in-memory cache keyed by file stem.

## API endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/` | Health check — returns `{"Hello": "World"}` |
| `GET` | `/items/{item_id}` | Example parameterised route |

## JSON output schema (per file)

```jsonc
{
  "file": {
    "name": "example.csv",
    "size_bytes": 12345,
    "row_count": 500,
    "column_count": 8
  },
  "columns": [
    {
      "name": "price",
      "dtype": "numeric",          // numeric | boolean | datetime | categorical | string
      "null_count": 2,
      "unique_count": 120,
      "top_values": ["9.99", "4.99", "14.99", "1.99", "7.99"],
      // numeric columns also include:
      "min": 1.99,
      "max": 99.99,
      "mean": 18.42,
      "std": 14.7,
      "median": 12.5
      // datetime columns include min/max as ISO strings instead
    }
  ]
}
```

## Adding an analyzer

See [analyzers/HOW_TO_ADD_ANALYZER.md](analyzers/HOW_TO_ADD_ANALYZER.md).

1. Create `analyzers/<name>.py` with a function `(df: pd.DataFrame, file_path: Path) -> dict`.
2. Import and append it to `ANALYZERS` in `analyzers/__init__.py`.

The returned dict is merged into the top-level JSON output automatically.

## Development setup

```bash
cd ..
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r data-dashboard-api/requirements.txt
```

API runs on `http://localhost:8000` by default.
