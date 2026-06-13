import json
import logging
from pathlib import Path

import pandas as pd

from analyzers import ANALYZERS

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)

INPUT_DIR = Path(__file__).parent / "input"
DATA_DIR = Path(__file__).parent / "data"


# ---------------------------------------------------------------------------
# Core pipeline
# ---------------------------------------------------------------------------

def analyze_csv(file_path: Path) -> tuple:
    total_steps = 1 + len(ANALYZERS) + 1  # read + analyzers + write
    step = 1
    logging.info("Step %d/%d — Reading CSV: %s", step, total_steps, file_path.name)
    df = pd.read_csv(file_path)
    logging.info("Loaded %d rows x %d columns", len(df), len(df.columns))

    result: dict = {}
    for analyzer in ANALYZERS:
        step += 1
        logging.info("Step %d/%d — Running: %s", step, total_steps, analyzer.__name__)
        result.update(analyzer(df, file_path))

    return result, total_steps, step


def main() -> None:
    DATA_DIR.mkdir(exist_ok=True)
    csv_files = list(INPUT_DIR.glob("*.csv"))

    if not csv_files:
        logging.warning("No CSV files found in %s", INPUT_DIR)
        return

    logging.info("Found %d CSV file(s) to process", len(csv_files))
    for csv_file in csv_files:
        logging.info("Processing: %s", csv_file.name)
        result, total_steps, step = analyze_csv(csv_file)
        output_path = DATA_DIR / f"{csv_file.stem}.json"
        step += 1
        logging.info("Step %d/%d — Writing output: %s", step, total_steps, output_path.name)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, default=str)
        logging.info("Done: %s", output_path)


if __name__ == "__main__":
    main()
