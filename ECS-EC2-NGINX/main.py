from modules.vpc import create_vpc, create_subnets, create_igw_and_route
from modules.security_group import create_security_groups
from modules.ec2 import launch_ec2
from modules.ecs_cluster import create_cluster
from modules.load_balancer import create_alb, create_target_group, create_listener
from modules.task_definition import register_task
from modules.ecs_service import create_service

import time

print("Creating VPC...")
vpc_id = create_vpc()

print("Creating Subnets...")
subnets = create_subnets(vpc_id)

print("Setting up Internet Gateway...")
create_igw_and_route(vpc_id, subnets)

print("Creating Security Groups...")
alb_sg, ec2_sg = create_security_groups(vpc_id)

print("Creating ECS Cluster...")
create_cluster()

print("Launching EC2...")
instance_id = launch_ec2(subnets[0], ec2_sg)

print("Waiting for EC2 to join ECS cluster...")
time.sleep(180)  # Wait for EC2 to be registered in ECS cluster

print("Creating ALB...")
alb_arn = create_alb(subnets, alb_sg)

print("Creating Target Group...")
tg_arn = create_target_group(vpc_id)

print("Creating Listener...")
create_listener(alb_arn, tg_arn)

print("Registering Task...")
task_def = register_task()

print("Creating ECS Service...")
create_service(task_def, tg_arn)

print(" DEPLOYMENT COMPLETE")