import boto3

def lambda_handler(event, context):
    ec2 = boto3.client('ec2', region_name='us-east-1')

    instance_id = 'i-084af17160454579d'  # replace

    # Get current state
    response = ec2.describe_instances(InstanceIds=[instance_id])
    state = response['Reservations'][0]['Instances'][0]['State']['Name']

    if state == 'running':
        ec2.stop_instances(InstanceIds=[instance_id])
        return "EC2 Stopped"

    elif state == 'stopped':
        ec2.start_instances(InstanceIds=[instance_id])
        return "EC2 Started"

    else:
        return f"Instance in {state} state"