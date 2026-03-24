import boto3
from botocore.exceptions import ClientError

bucket_name = 'sneha-demo-bucket-2424-unique'

try:
    s3 = boto3.client('s3', region_name='us-east-1')

    s3.delete_bucket(Bucket=bucket_name)

    print(f"Bucket '{bucket_name}' deleted successfully.")

except ClientError as e:
    print("Error:", e)
except Exception as e:
    print("Other Error:", e)