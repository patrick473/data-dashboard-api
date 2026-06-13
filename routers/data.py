import json
import re
from pathlib import Path

from fastapi import APIRouter, HTTPException

DATA_DIR = Path(__file__).parent.parent / "data"

router = APIRouter(prefix="/data", tags=["data"])


@router.get("/available-files")
def get_available_files():
    files = [f.stem for f in DATA_DIR.glob("*.json")]
    return {"available_files": files}


@router.get("/{filename}")
def get_data(filename: str):
    if not re.fullmatch(r"[\w\-]+", filename):
        raise HTTPException(status_code=400, detail="Invalid filename")

    file_path = (DATA_DIR / f"{filename}.json").resolve()

    if not str(file_path).startswith(str(DATA_DIR.resolve())):
        raise HTTPException(status_code=400, detail="Invalid filename")

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    return json.loads(file_path.read_text(encoding="utf-8"))
