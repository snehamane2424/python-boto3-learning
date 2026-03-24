import boto3
from botocore.exceptions import ClientError

topic_arn = 'arn:aws:sns:us-east-1:111236691973:s3-upload-topic'

try:
    sns = boto3.client('sns', region_name='us-east-1')

    sns.delete_topic(TopicArn=topic_arn)

    print("Snehaaa Topic deleted successfully.")

except ClientError as e:
    print("Error:", e)
except Exception as e:
    print("Other Error:", e)