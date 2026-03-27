import boto3
from config import REGION

elbv2 = boto3.client("elbv2", region_name=REGION)

def create_alb(subnets, sg_id):
    alb = elbv2.create_load_balancer(
        Name='my-alb',
        Subnets=subnets,
        SecurityGroups=[sg_id],
        Scheme='internet-facing',
        Type='application'
    )
    return alb['LoadBalancers'][0]['LoadBalancerArn']


def create_target_group(vpc_id):
    tg = elbv2.create_target_group(
        Name='nginx-tg',
        Protocol='HTTP',
        Port=80,
        VpcId=vpc_id,
        HealthCheckProtocol='HTTP',
        HealthCheckPath='/',
        HealthCheckPort='traffic-port',
        Matcher={'HttpCode': '200'},
        TargetType='instance'
    )
    return tg['TargetGroups'][0]['TargetGroupArn']


def create_listener(alb_arn, tg_arn):
    elbv2.create_listener(
        LoadBalancerArn=alb_arn,
        Protocol='HTTP',
        Port=80,
        DefaultActions=[
            {
                'Type': 'forward',
                'TargetGroupArn': tg_arn
            }
        ]
    )