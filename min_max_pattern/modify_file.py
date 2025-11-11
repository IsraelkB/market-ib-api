import pandas as pd
from utills.time import duration_in_minutes

def filter_by_time_and_extreme(df: pd.DataFrame, is_min: bool, value_cols,
                               time_col: str = "date", threshold_minutes: int = 2) -> pd.DataFrame:
    """
    Filters a DataFrame by keeping only one row (either the minimum or maximum)
    when multiple rows occur within a specified time window. The comparison can
    be based on one or multiple value columns (e.g., 'open' and 'close').

    Parameters
    ----------
    df : pd.DataFrame
        The input DataFrame containing a datetime column and a value column.
    is_min : bool
        Determines which row to keep if multiple rows fall within the threshold.
        True = keep the minimum row, False = keep the maximum row.
    value_cols : str or list[str]
        Column name(s) to use when determining the minimum or maximum.
        If multiple columns are given, the extreme value will be computed across them.
    time_col : str, optional
        The name of the datetime column. Default is "date".
    threshold_minutes : int, optional
        The maximum allowed difference in minutes between two rows to be considered
        part of the same group. Default is 6.

    Returns
    -------
    pd.DataFrame
        A filtered DataFrame containing only the selected (min or max) rows per time group.
    """
    df = df.copy()
    df[time_col] = pd.to_datetime(df[time_col], utc=True)
    df = df.sort_values(by=time_col).reset_index(drop=True)

    if isinstance(value_cols, str):
        value_cols = [value_cols]

    to_keep = []
    i = 0
    while i < len(df):
        curr_row = df.iloc[i]
        group = [curr_row]

        j = i + 1
        while j < len(df):
            next_row = df.iloc[j]
            delta = duration_in_minutes(curr_row[time_col], next_row[time_col])
            if delta <= threshold_minutes:
                group.append(next_row)
                j += 1
            else:
                break
            curr_row = next_row

        group_df = pd.DataFrame(group)

        if is_min:
            chosen = group_df.loc[group_df[value_cols].min(axis=1).idxmin()]
        else:
            chosen = group_df.loc[group_df[value_cols].max(axis=1).idxmax()]

        to_keep.append(chosen)
        i = j

    return pd.DataFrame(to_keep).reset_index(drop=True)
