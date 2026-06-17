from typing import Callable

import pandas as pd

from .base import analyze_base
from .numeric import analyze_numeric
from .quartiles import analyze_quartiles
from .shape import analyze_shape
from .value_flags import analyze_value_flags
from .datetime import analyze_datetime
from .distribution import analyze_distribution
from .frequency import analyze_frequency
from .temporal_distribution import analyze_temporal_distribution
from .gap_stats import analyze_gap_stats

COLUMN_ANALYZERS: list[Callable[[pd.Series, str], dict]] = [
    analyze_base,
    analyze_numeric,
    analyze_quartiles,
    analyze_shape,
    analyze_value_flags,
    analyze_datetime,
    analyze_distribution,
    analyze_frequency,
    analyze_temporal_distribution,
    analyze_gap_stats,
]
