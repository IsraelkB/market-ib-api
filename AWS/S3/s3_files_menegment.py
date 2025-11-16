import boto3
import pandas as pd
from io import StringIO
from AWS.S3.s3_client import create_s3_client
from config import aws_credentials_settings

bucket_name = aws_credentials_settings.bucket_name
s3 = create_s3_client()

def load_all_data_from_s3_once(prefix):
    """
    loaded all files from prefix once (for example: reports/min_max/).
    return dict: { 'AAPL': df, 'TSLA': df, ... }
    """
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
    result = {}

    for obj in response.get("Contents", []):
        key = obj["Key"]

        stock = key.split("/")[-1]

        file_data = s3.get_object(Bucket=bucket_name, Key=key)["Body"].read().decode("utf-8")
        df = pd.read_csv(StringIO(file_data))

        result[stock] = df

    return result


def open_file_to_read_s3(file_path: str) -> pd.DataFrame:
    """
    reding CSV file from S3 and reformat him to DataFrame.
    """
    key = f"{file_path}.csv" if not file_path.endswith(".csv") else file_path
    try:
        obj = s3.get_object(Bucket=bucket_name, Key=key)
        df = pd.read_csv(obj["Body"])
        return df
    except s3.exceptions.NoSuchKey:
        return pd.DataFrame()
    except Exception as e:
        print(f"❌ Error reading {key} from S3: {e}")
        return pd.DataFrame()


def update_file_s3(df: pd.DataFrame, file_path: str):
    """
    reading as CSV from S3 and reformat him to DataFrame.
    """
    key = f"{file_path}.csv" if not file_path.endswith(".csv") else file_path
    try:
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False)
        s3.put_object(Bucket=bucket_name, Key=key, Body=csv_buffer.getvalue())
        print(f"✅ Updated {key} in S3.")
    except Exception as e:
        print(f"❌ Error writing {key} to S3: {e}")


# # test for functions
# rgti_file = open_file_to_read_s3("reports/doubles/rgti_test.csv")
# print(rgti_file)
# update_alert_file_s3(rgti_file, "reports/doubles/rgti_test.csv")