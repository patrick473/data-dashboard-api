import pandas as pd

DAY_NAMES = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def analyze_temporal_distribution(series: pd.Series, dtype: str) -> dict:
    if dtype != "datetime":
        return {}

    parsed = pd.to_datetime(series, errors="coerce").dropna()
    if parsed.empty:
        return {}

    dow_counts = parsed.dt.dayofweek.value_counts().reindex(range(7), fill_value=0)
    hour_counts = parsed.dt.hour.value_counts().reindex(range(24), fill_value=0)

    return {
        "day_of_week": [
            {"day": DAY_NAMES[i], "count": int(dow_counts[i])}
            for i in range(7)
        ],
        "hour_of_day": [
            {"hour": i, "count": int(hour_counts[i])}
            for i in range(24)
        ],
    }
