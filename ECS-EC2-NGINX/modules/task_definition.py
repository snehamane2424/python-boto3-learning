import boto3
from config import REGION

ecs = boto3.client("ecs", region_name=REGION)

def register_task():

    response = ecs.register_task_definition(
        family='nginx-task',
        networkMode='bridge',
        requiresCompatibilities=["EC2"],  # ✅ IMPORTANT
        cpu='256',
        memory='256',
        containerDefinitions=[
            {
                "name": "nginx",
                "image": "nginx",
                "essential": True,
                "portMappings": [
                    {
                        "containerPort": 80,
                        "hostPort": 80
                    }
                ]
            }
        ]
    )

    return response['taskDefinition']['taskDefinitionArn']