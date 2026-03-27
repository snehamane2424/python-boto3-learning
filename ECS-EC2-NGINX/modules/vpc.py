import boto3
from config import REGION, VPC_CIDR, SUBNET_CIDRS

ec2 = boto3.client("ec2", region_name=REGION)

def create_vpc():
    vpc = ec2.create_vpc(CidrBlock=VPC_CIDR)
    vpc_id = vpc['Vpc']['VpcId']

    ec2.modify_vpc_attribute(VpcId=vpc_id, EnableDnsSupport={'Value': True})
    ec2.modify_vpc_attribute(VpcId=vpc_id, EnableDnsHostnames={'Value': True})

    return vpc_id


def create_subnets(vpc_id):
    subnets = []
    azs = ec2.describe_availability_zones()['AvailabilityZones']

    for i, cidr in enumerate(SUBNET_CIDRS):
        subnet = ec2.create_subnet(
            VpcId=vpc_id,
            CidrBlock=cidr,
            AvailabilityZone=azs[i]['ZoneName']
        )
        subnet_id = subnet['Subnet']['SubnetId']

        ec2.modify_subnet_attribute(
            SubnetId=subnet_id,
            MapPublicIpOnLaunch={"Value": True}
        )

        subnets.append(subnet_id)

    return subnets


def create_igw_and_route(vpc_id, subnets):
    igw = ec2.create_internet_gateway()
    igw_id = igw['InternetGateway']['InternetGatewayId']

    ec2.attach_internet_gateway(VpcId=vpc_id, InternetGatewayId=igw_id)

    rt = ec2.create_route_table(VpcId=vpc_id)
    rt_id = rt['RouteTable']['RouteTableId']

    ec2.create_route(
        RouteTableId=rt_id,
        DestinationCidrBlock="0.0.0.0/0",
        GatewayId=igw_id
    )

    for subnet in subnets:
        ec2.associate_route_table(
            SubnetId=subnet,
            RouteTableId=rt_id
        )