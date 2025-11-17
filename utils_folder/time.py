import pandas as pd
from datetime import timezone

def duration_in_minutes(early_time, late_time):
    early_time = early_time.astimezone(timezone.utc)
    late_time = late_time.astimezone(timezone.utc)
    duration = late_time - early_time
    return duration.total_seconds() / 60


def invert_gtc(df, time_columns):
    for col in time_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce", utc=True)
            df[col] = df[col].dt.tz_convert("Asia/Jerusalem")