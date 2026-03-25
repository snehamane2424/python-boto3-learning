import boto3

# Create IAM client
iam = boto3.client('iam')

# Create user
response = iam.create_user(
    UserName='test-user-boto3'
)

print("User Created Successfully!")
print(response)

# Step 2: Attach policy
iam.attach_user_policy(
    UserName='test-user-boto3',
    PolicyArn='arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess'
)

print("Policy attached")