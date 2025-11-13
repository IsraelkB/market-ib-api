import pandas as pd

def duration_in_minutes(arly_time, late_time):
    duration = late_time - arly_time
    return duration.total_seconds() / 60

def invert_gtc(df, time_columns):
    for col in time_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce", utc=True)
            df[col] = df[col].dt.tz_convert("Asia/Jerusalem")