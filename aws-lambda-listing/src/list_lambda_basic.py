import boto3

# Step 1: Create Lambda client
client = boto3.client('lambda')

# Step 2: Call AWS API
response = client.list_functions()

# Step 3: Print full JSON response
print(response)