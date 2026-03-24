import boto3
from botocore.exceptions import ClientError
from datetime import datetime, timezone
import os

bucket_name = 'sneha-demo-bucket-2424-unique'
file_path = 'project_file.txt'
object_name = 'project_file.txt'
topic_arn = 'arn:aws:sns:us-east-1:111236691973:s3-upload-topic'
region = 'us-east-1'

try:
    s3 = boto3.client('s3', region_name=region)
    sns = boto3.client('sns', region_name=region)

    # Step 1: Upload file to S3
    s3.upload_file(file_path, bucket_name, object_name)
    print(f"File '{file_path}' uploaded to S3 bucket '{bucket_name}'.")

    # Step 2: Get file size from local file
    file_size = os.path.getsize(file_path)

    # Step 3: Get upload time
    upload_time = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')

    # Step 4: Create notification message
    message = f"""
A new file has been uploaded to S3.

Bucket Name: {bucket_name}
Object Name: {object_name}
Object Size: {file_size} bytes
Upload Time: {upload_time}
Region: {region}
"""

    # Step 5: Publish message to SNS
    response = sns.publish(
        TopicArn=topic_arn,
        Subject='S3 File Upload Notification',
        Message=message
    )

    print("SNS notification sent successfully.")
    print("Message ID:", response['MessageId'])

except ClientError as e:
    print("AWS Error:", e)
except FileNotFoundError:
    print("The local file was not found.")
except Exception as e:
    print("Other Error:", e)