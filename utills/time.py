def duration_in_minutes(arly_time, Late_time):
    duration = Late_time - arly_time
    return duration.total_seconds() / 60

