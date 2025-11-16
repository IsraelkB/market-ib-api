from AWS.S3.s3_files_menegment import open_file_to_read_s3, update_file_s3
from min_max_pattern.data_rectification_methods import connect_dfss
from utils_folder.get_files import open_file_to_read, open_file_to_write


def connect_data(relative_path, drop_columns):
    cloud_data = open_file_to_read_s3(relative_path)
    local_data = open_file_to_read(relative_path)  # local
    df_combined = connect_dfss(local_data, cloud_data, drop_columns)
    update_file_s3(df_combined, relative_path)
    open_file_to_write(relative_path, df_combined)
    return df_combined

def connect_local_cloud_data(stocks):
    for stock in stocks:
        min_max_file_path = f"reports/min_max/{stock}"
        stock_data_path = f"reports/daily_activity/{stock}"
        file_alert = f"reports/doubles/{stock}"
        connect_data(min_max_file_path, ["date", "type"])
        connect_data(stock_data_path, ["date"])
        connect_data(file_alert, ["date_early", "date_late"])
