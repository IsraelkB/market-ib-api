from AWS.S3.s3_files_menegment import open_file_to_read_s3, update_file_s3, load_all_data_from_s3_once
from min_max_pattern.data_rectification_methods import connect_dfss
from utils_folder.get_files import open_file_to_read, open_file_to_write, get_local_stock_list


# def connect_data(relative_path, drop_columns):
#     cloud_data = open_file_to_read_s3(relative_path)
#     local_data = open_file_to_read(relative_path)  # local
#     df_combined = connect_dfss(local_data, cloud_data, drop_columns)
#     update_file_s3(df_combined, relative_path)
#     open_file_to_write(relative_path, df_combined)
#     return df_combined

# def connect_local_cloud_data(stocks):
#     for stock in stocks:
#         min_max_file_path = f"reports/min_max/{stock}"
#         stock_data_path = f"reports/daily_activity/{stock}"
#         file_alert = f"reports/doubles/{stock}"
#         connect_data(min_max_file_path, ["date", "type"])
#         connect_data(stock_data_path, ["date"])
#         connect_data(file_alert, ["date_early", "date_late"])


def process_all_groups(cloud_stocks):
    processed = {}

    for group_name, cloud_stocks_map in cloud_stocks.items():

        processed[group_name] = {}
        local_folder = f"reports/{group_name}/"

        local_stocks = get_local_stock_list(local_folder)

        for stock in local_stocks:
            local_df = open_file_to_read(f"{local_folder}{stock}")

            cloud_df = cloud_stocks_map.get(stock)

            drop_cols = {
                "min_max": ["date", "type"],
                "daily": ["date"],
                "doubles": ["date_early", "date_late"],
            }[group_name]

            df_combined = connect_dfss(local_df, cloud_df, drop_cols)
            processed[group_name][stock] = df_combined
    return processed


def load_all_stocks_from_s3():
    return {
        "min_max": load_all_data_from_s3_once("reports/min_max/"),
        "daily": load_all_data_from_s3_once("reports/daily_activity/"),
        "doubles": load_all_data_from_s3_once("reports/doubles/"),
    }


def write_all_groups(processed):
    for group_name, stocks_map in processed.items():
        for stock, df in stocks_map.items():
            path = f"reports/{group_name}/{stock}"
            update_file_s3(df, path)
            open_file_to_write(path, df)


def connect_local_cloud_data_batch(stocks):
    groups = load_all_stocks_from_s3()
    processed = process_all_groups(groups)
    write_all_groups(processed)