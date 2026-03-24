import boto3
from botocore.exceptions import ClientError

topic_name = 's3-upload-topic'

try:
    sns = boto3.client('sns', region_name='us-east-1')

    response = sns.create_topic(Name=topic_name)

    print("Topic created successfully.")
    print("Topic ARN:", response['TopicArn'])

except ClientError as e:
    print("Error:", e)
except Exception as e:
    print("Other Error:", e)