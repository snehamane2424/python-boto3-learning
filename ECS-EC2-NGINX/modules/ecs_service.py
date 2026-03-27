import boto3
from config import REGION, CLUSTER_NAME

ecs = boto3.client("ecs", region_name=REGION)

def create_service(task_def_arn, tg_arn):

    services = ecs.list_services(cluster=CLUSTER_NAME)['serviceArns']

    if any("nginx-service" in s for s in services):
        print("Service already exists")
        return

    ecs.create_service(
        cluster=CLUSTER_NAME,
        serviceName="nginx-service",
        taskDefinition=task_def_arn,
        desiredCount=1,
        launchType="EC2",
        loadBalancers=[
            {
                "targetGroupArn": tg_arn,
                "containerName": "nginx",
                "containerPort": 80
            }
        ]
    )