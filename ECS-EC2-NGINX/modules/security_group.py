import boto3
from config import REGION

ec2 = boto3.client("ec2", region_name=REGION)

def create_security_groups(vpc_id):

    # ALB SG
    alb_sg = ec2.create_security_group(
        GroupName="alb-sg",
        Description="ALB SG",
        VpcId=vpc_id
    )
    alb_sg_id = alb_sg['GroupId']

    ec2.authorize_security_group_ingress(
        GroupId=alb_sg_id,
        IpPermissions=[
            {
                'IpProtocol': 'tcp',
                'FromPort': 80,
                'ToPort': 80,
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
            }
        ]
    )

    # EC2 SG
    ec2_sg = ec2.create_security_group(
        GroupName="ec2-sg",
        Description="EC2 SG",
        VpcId=vpc_id
    )
    ec2_sg_id = ec2_sg['GroupId']

    ec2.authorize_security_group_ingress(
        GroupId=ec2_sg_id,
        IpPermissions=[
            {
                'IpProtocol': 'tcp',
                'FromPort': 80,
                'ToPort': 80,
                'UserIdGroupPairs': [{'GroupId': alb_sg_id}]
            },
            {
                'IpProtocol': 'tcp',
                'FromPort': 22,
                'ToPort': 22,
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
            }
        ]
    )

    return alb_sg_id, ec2_sg_id