import boto3
from botocore.exceptions import ClientError

bucket_name = 'sneha-demo-bucket-2424-unique'
object_name = 'project_file.txt'

try:
    s3 = boto3.client('s3', region_name='us-east-1')

    s3.delete_object(Bucket=bucket_name, Key=object_name)

    print(f"Object '{object_name}' deleted successfully.")

except ClientError as e:
    print("Error:", e)
except Exception as e:
    print("Other Error:", e)