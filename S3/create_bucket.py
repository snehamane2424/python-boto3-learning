import boto3
from botocore.exceptions import ClientError

bucket_name = 'sneha-demo-bucket-2424-unique' 

try:
    s3 = boto3.client('s3', region_name='us-east-1')

    response = s3.create_bucket(
        Bucket=bucket_name
    )

    print(f"Bucket '{bucket_name}' created successfully")
    print(response)

except ClientError as e:
    print("AWS Error:", e)
except Exception as e:
    print("Other Error:", e)