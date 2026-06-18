import json
import re
from pathlib import Path

from fastapi import APIRouter, HTTPException

RESULTS_DIR = Path(__file__).parent.parent / "models" / "results"

router = APIRouter(prefix="/models", tags=["models"])


@router.get("/")
def get_available_models():
    models = [f.stem.removesuffix("_results") for f in RESULTS_DIR.glob("*.json")]
    return {"available_models": models}


@router.get("/{model_name}")
def get_model_results(model_name: str):
    if not re.fullmatch(r"[\w\-]+", model_name):
        raise HTTPException(status_code=400, detail="Invalid model name")

    file_path = (RESULTS_DIR / f"{model_name}_results.json").resolve()

    if not str(file_path).startswith(str(RESULTS_DIR.resolve())):
        raise HTTPException(status_code=400, detail="Invalid model name")

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Model not found")

    return json.loads(file_path.read_text(encoding="utf-8"))
