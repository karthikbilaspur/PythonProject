import boto3
from botocore.exceptions import ClientError

class Ec2Instances:
    def __init__(self, region_name):
        self.ec2 = boto3.client('ec2', region_name=region_name)

    def delete_snapshots(self, days):
        """Delete snapshots older than specified days"""
        # implementation remains the same
        pass

    def delete_available_volumes(self):
        """Delete available volumes"""
        # implementation remains the same
        pass

    def shutdown(self):
        """Shutdown EC2 instances"""
        # implementation remains the same
        pass


class Rds:
    def __init__(self, region_name):
        self.rds = boto3.client('rds', region_name=region_name)

    def cleanup_snapshot(self):
        """Cleanup RDS snapshots"""
        # implementation remains the same
        pass

    def cleanup_instances(self):
        """Cleanup RDS instances"""
        # implementation remains the same
        pass


def lambda_handler(event, context):
    """AWS Lambda function handler"""
    print(f"Event: {event}")
    print(f"Context: {context}")

    ec2_regions = boto3.client('ec2')
    try:
        regions_response = ec2_regions.describe_regions()
        regions = regions_response['Regions']
    except ClientError as e:
        print(f"Failed to describe regions: {e}")
        return {
            'statusCode': 500,
            'body': 'Failed to describe regions'
        }

    deleted_snapshot_counts = {}

    for region in regions:
        region_name = region['RegionName']
        try:
            instances = Ec2Instances(region_name)
            deleted_counts = instances.delete_snapshots(1)
            instances.delete_available_volumes()
            instances.shutdown()

            rds = Rds(region_name)
            rds.cleanup_snapshot()
            rds.cleanup_instances()

            deleted_snapshot_counts[region_name] = deleted_counts
            print(f"Deleted snapshot counts for region {region_name}: {deleted_counts}")
        except ClientError as e:
            print(f"Error processing region {region_name}: {e}")

    return {
        'statusCode': 200,
        'body': 'Snapshot cleanup completed',
        'deletedSnapshotCounts': deleted_snapshot_counts
    }