import boto3
from botocore.exceptions import ClientError

topic_arn = 'arn:aws:sns:us-east-1:111236691973:s3-upload-topic'

try:
    sns = boto3.client('sns', region_name='us-east-1')

    response = sns.publish(
        TopicArn=topic_arn,
        Subject='Test Notification from boto3',
        Message='Hello Snehaaaa! This is a test SNS message sent using boto3.'
    )

    print("Message published successfully.")
    print("Message ID:", response['MessageId'])

except ClientError as e:
    print("Error:", e)
except Exception as e:
    print("Other Error:", e)