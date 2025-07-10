import boto3

def create_ec2(client, ami_id, count):
    try:
        response = client.run_instances(ImageId=ami_id, MinCount=count, MaxCount=count)
        instance_ids = [instance['InstanceId'] for instance in response['Instances']]
        print(f"Created {count} EC2 instances with IDs: {instance_ids}")
        return instance_ids
    except Exception as e:
        print(f"Error creating EC2 instances: {str(e)}")
        return None

def create_ec2_snapshots(client, volume_id):
    try:
        response = client.create_snapshot(VolumeId=volume_id)
        snapshot_id = response['SnapshotId']
        print(f"Created snapshot {snapshot_id} for volume {volume_id}")
        return snapshot_id
    except Exception as e:
        print(f"Error creating snapshot: {str(e)}")
        return None

def create_ec2_volume(client, availability_zone, size=10):
    try:
        response = client.create_volume(AvailabilityZone=availability_zone, Size=size)
        volume_id = response['VolumeId']
        print(f"Created volume {volume_id} in {availability_zone}")
        return volume_id
    except Exception as e:
        print(f"Error creating volume: {str(e)}")
        return None

def create_vpc(client, cidr_block):
    try:
        response = client.create_vpc(CidrBlock=cidr_block)
        vpc_id = response['Vpc']['VpcId']
        print(f"Created VPC {vpc_id} with CIDR block {cidr_block}")
        return vpc_id
    except Exception as e:
        print(f"Error creating VPC: {str(e)}")
        return None

