import boto3
from botocore.exceptions import ClientError
import os

bucket_name = 'sneha-demo-bucket-2424-unique'
file_path = 'project_file.txt'
object_name = 'project_file.txt'
topic_arn = 'arn:aws:sns:us-east-1:111236691973:s3-upload-topic'
region = 'us-east-1'

try:
    s3 = boto3.client('s3', region_name=region)
    sns = boto3.client('sns', region_name=region)

    # Upload file
    s3.upload_file(file_path, bucket_name, object_name)
    print(f"File '{file_path}' uploaded successfully.")

    # Get object metadata from S3
    response = s3.head_object(Bucket=bucket_name, Key=object_name)

    object_size = response['ContentLength']
    last_modified = response['LastModified']

    message = f"""
A new object has been uploaded to S3.

Bucket Name: {bucket_name}
Object Name: {object_name}
Object Size: {object_size} bytes
Last Modified: {last_modified}
Region: {region}
"""

    sns_response = sns.publish(
        TopicArn=topic_arn,
        Subject='S3 Upload Notification with Metadata',
        Message=message
    )

    print("SNS notification sent successfully.")
    print("Message ID:", sns_response['MessageId'])

except ClientError as e:
    print("AWS Error:", e)
except FileNotFoundError:
    print("Local file not found.")
except Exception as e:
    print("Other Error:", e)