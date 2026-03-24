import boto3
from botocore.exceptions import ClientError

bucket_name = 'sneha-demo-bucket-2424-unique'
object_name = 'msg.txt'
download_path = 'downloaded_msg.txt'

try:
    s3 = boto3.client('s3', region_name='us-east-1')

    s3.download_file(bucket_name, object_name, download_path)

    print(f"File '{object_name}' downloaded successfully as '{download_path}'.")

except ClientError as e:
    print("Error:", e)
except Exception as e:
    print("Other Error:", e)