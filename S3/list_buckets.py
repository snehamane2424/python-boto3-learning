import boto3
from botocore.exceptions import ClientError

try:
    s3 = boto3.client('s3')
    response = s3.list_buckets()

    print("Available S3 buckets:")
    for bucket in response['Buckets']:
        print(bucket['Name'])

except ClientError as e:
    print("Error:", e)
except Exception as e:
    print("Other Error:", e)