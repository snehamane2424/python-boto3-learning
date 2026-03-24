import boto3
from botocore.exceptions import ClientError

try:
    sns = boto3.client('sns', region_name='us-east-1')

    response = sns.list_topics()

    print("Available SNS topics:")
    for topic in response['Topics']:
        print(topic['TopicArn'])

except ClientError as e:
    print("Error:", e)
except Exception as e:
    print("Other Error:", e)