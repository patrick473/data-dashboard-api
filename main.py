from contextlib import asynccontextmanager
from pathlib import Path

import pandas as pd
from fastapi import FastAPI

DATA_DIR = Path(__file__).parent / "data"

# Keyed by stem filename, e.g. "my_file" for "my_file.csv"
csv_cache: dict[str, pd.DataFrame] = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    DATA_DIR.mkdir(exist_ok=True)
    for csv_file in DATA_DIR.glob("*.csv"):
        csv_cache[csv_file.stem] = pd.read_csv(csv_file)
        print(f"Loaded {csv_file.name} ({len(csv_cache[csv_file.stem])} rows)")
    yield
    csv_cache.clear()


app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}