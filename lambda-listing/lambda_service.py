import boto3
from config import REGION


def get_lambda_client():
    return boto3.client('lambda', region_name=REGION)


def list_all_functions():
    client = get_lambda_client()

    paginator = client.get_paginator('list_functions')

    functions = []

    for page in paginator.paginate():
        for func in page['Functions']:
            functions.append(func)

    return functions