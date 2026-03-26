import boto3

client = boto3.client('lambda')

response = client.list_functions()

functions = response['Functions']

for func in functions:
    print("Function Name:", func['FunctionName'])
    print("Runtime:", func['Runtime'])
    print("Memory:", func['MemorySize'])
    print("Last Modified:", func['LastModified'])
    print("-" * 40)