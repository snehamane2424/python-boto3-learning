import boto3
from botocore.exceptions import ClientError

bucket_name = 'sneha-demo-bucket-2424-unique'
file_path = 'msg.txt'
object_name = 'msg.txt'

try:
    s3 = boto3.client('s3', region_name='us-east-1')

    s3.upload_file(file_path, bucket_name, object_name)

    print(f"File '{file_path}' uploaded successfully to bucket '{bucket_name}'.")

except ClientError as e:
    print("Error:", e)
except FileNotFoundError:
    print("Local file not found.")
except Exception as e:
    print("Other Error:", e)