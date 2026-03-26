import boto3

client = boto3.client('lambda')

paginator = client.get_paginator('list_functions')

for page in paginator.paginate():
    for func in page['Functions']:
        print(func['FunctionName'])