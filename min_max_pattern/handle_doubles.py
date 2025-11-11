from min_max_pattern.data_rectification import connect_dfs, modify_date
from allerts.mail_allerts import send_email
from min_max_pattern.double_pattern import find_double_top, find_double_bottom
from min_max_pattern.utils import update_alert_file
from utills.get_files import open_file_to_read
import pandas as pd

def detect_for_doubles(df_min, df_max, stock_name):
    file_alert = f"reports/doubles/{stock_name}"
    df_double_alerted = open_file_to_read(file_alert)
    double_top_list = find_double_top(df_max)
    double_bottom_list = find_double_bottom(df_min)

    def build_message(stock_name, event_type, event_df):
        date_early = event_df.loc[0, 'date_early']
        date_late = event_df.loc[0, 'date_late']
        msg = (
            f"📈 התראה עבור מניה: {stock_name}\n\n"
            f"התרחש {event_type.upper()} בין הנרות בתאריכים הבאים:\n"
            f"{date_early} - {date_late}"
        )
        return msg

    def is_event_already_alerted(event_df, alerted_df):
        if alerted_df.empty:
            return False

        alerted_df = alerted_df.copy()
        alerted_df['date_early'] = pd.to_datetime(alerted_df['date_early'], utc=True, errors='coerce')
        alerted_df['date_late'] = pd.to_datetime(alerted_df['date_late'], utc=True, errors='coerce')

        date_early = pd.to_datetime(event_df.loc[0, 'date_early'], utc=True)
        date_late = pd.to_datetime(event_df.loc[0, 'date_late'], utc=True)

        return (
                (alerted_df['date_early'] == date_early) &
                (alerted_df['date_late'] == date_late)
        ).any()

    def combine_events(double):
        early = event[0].rename(lambda col: f"{col}_early").to_frame().T.reset_index(drop=True)
        late = event[1].rename(lambda col: f"{col}_late").to_frame().T.reset_index(drop=True)
        combined = pd.concat([early, late], axis=1)
        return combined

    for event in double_top_list:
        event_df = combine_events(event)
        if not is_event_already_alerted(event_df, df_double_alerted):
            message = build_message(stock_name, "Double Top", event_df)
            print(message)
            # send_email(f"{stock_name} alert - DOUBLE TOP",message)
            df_double_alerted = pd.concat([df_double_alerted, event_df], ignore_index=True)

    for event in double_bottom_list:
        event_df = combine_events(event)
        if not is_event_already_alerted(event_df, df_double_alerted):
            message = build_message(stock_name, "Double Bottom", event_df)
            print(message)
            # send_email(f"{stock_name} alert - DOUBLE BOTTOM", message)
            df_double_alerted = pd.concat([df_double_alerted, event_df], ignore_index=True)
    update_alert_file(df_double_alerted, file_alert)