import boto3
from config import REGION, INSTANCE_TYPE, KEY_NAME, CLUSTER_NAME

ec2 = boto3.client("ec2", region_name=REGION)
ssm = boto3.client("ssm", region_name=REGION)


# ✅ Get latest ECS Optimized AMI (VERY IMPORTANT)
def get_latest_ecs_ami():
    param = ssm.get_parameter(
        Name="/aws/service/ecs/optimized-ami/amazon-linux-2/recommended/image_id"
    )
    return param['Parameter']['Value']


def launch_ec2(subnet_id, sg_id):

    ami_id = get_latest_ecs_ami()

    # ✅ FIXED USER DATA (ECS agent setup)
    user_data = f"""#!/bin/bash
echo ECS_CLUSTER={CLUSTER_NAME} >> /etc/ecs/ecs.config
yum install -y ecs-init
systemctl enable ecs
systemctl start ecs
"""

    response = ec2.run_instances(
        ImageId=ami_id,
        InstanceType=INSTANCE_TYPE,
        MinCount=1,
        MaxCount=1,
        KeyName=KEY_NAME,
        SecurityGroupIds=[sg_id],
        SubnetId=subnet_id,
        UserData=user_data,
        IamInstanceProfile={'Name': 'ecsInstanceRole'}
    )

    return response['Instances'][0]['InstanceId']