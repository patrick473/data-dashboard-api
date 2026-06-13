from pathlib import Path
from typing import Callable

import pandas as pd

from .file_metadata import analyze_file_metadata
from .columns import analyze_columns
from .completeness import analyze_completeness

# Registry — append new analyzer functions here to add more analytics
ANALYZERS: list[Callable[[pd.DataFrame, Path], dict]] = [
    analyze_file_metadata,
    analyze_columns,
    analyze_completeness
]
