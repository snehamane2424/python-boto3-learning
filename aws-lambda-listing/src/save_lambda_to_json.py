import boto3
import json

client = boto3.client('lambda')

response = client.list_functions()

result = []

for func in response['Functions']:
    result.append({
        "name": func['FunctionName'],
        "runtime": func['Runtime'],
        "memory": func['MemorySize'],
        "last_modified": func['LastModified']
    })

# Save to file
with open('output/lambda_functions.json', 'w') as f:
    json.dump(result, f, indent=4)

print("Saved to output/lambda_functions.json")