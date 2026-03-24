import boto3
from botocore.exceptions import ClientError

topic_arn = 'arn:aws:sns:us-east-1:111236691973:s3-upload-topic'
email_address = 'sneha.mane@virtuecloud.io'

try:
    sns = boto3.client('sns', region_name='us-east-1')

    response = sns.subscribe(
        TopicArn=topic_arn,
        Protocol='email',
        Endpoint=email_address
    )

    print("Subscription requested successfully.")
    print("Subscription ARN:", response['SubscriptionArn'])
    print("Please check your email and confirm the subscription.")

except ClientError as e:
    print("Error:", e)
except Exception as e:
    print("Other Error:", e)