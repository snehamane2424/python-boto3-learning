import boto3
from botocore.exceptions import ClientError

bucket_name = 'sneha-demo-bucket-2424-unique'

try:
    s3 = boto3.client('s3', region_name='us-east-1')

    response = s3.list_objects_v2(Bucket=bucket_name)

    if 'Contents' in response:
        print(f"Objects in bucket '{bucket_name}':")
        for obj in response['Contents']:
            print("Key:", obj['Key'])
            print("Size:", obj['Size'], "bytes")
            print("Last Modified:", obj['LastModified'])
            print("-" * 30)
    else:
        print("Bucket is empty.")

except ClientError as e:
    print("Error:", e)
except Exception as e:
    print("Other Error:", e)