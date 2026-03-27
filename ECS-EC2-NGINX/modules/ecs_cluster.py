import boto3
from config import REGION, CLUSTER_NAME

ecs = boto3.client("ecs", region_name=REGION)

def create_cluster():
    clusters = ecs.list_clusters()['clusterArns']

    if any(CLUSTER_NAME in c for c in clusters):
        print("Cluster already exists")
    else:
        ecs.create_cluster(clusterName=CLUSTER_NAME)