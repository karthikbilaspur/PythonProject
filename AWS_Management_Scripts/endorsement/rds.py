import boto3
from datetime import datetime, timedelta

class RDSManager:
    def __init__(self, region):
        self.rds = boto3.client('rds', region_name=region)

    def list_instances(self, status=None):
        instances = self.rds.describe_db_instances()
        if status:
            return [instance for instance in instances['DBInstances'] if instance['DBInstanceStatus'] == status]
        return instances['DBInstances']

    def list_snapshots(self, status=None):
        snapshots = self.rds.describe_db_snapshots()
        if status:
            return [snapshot for snapshot in snapshots['DBSnapshots'] if snapshot['Status'] == status]
        return snapshots['DBSnapshots']

    def start_instance(self, instance_id):
        try:
            self.rds.start_db_instance(DBInstanceIdentifier=instance_id)
            print(f"Instance {instance_id} started successfully")
        except Exception as e:
            print(f"Error starting instance {instance_id}: {str(e)}")

    def stop_instance(self, instance_id):
        try:
            self.rds.stop_db_instance(DBInstanceIdentifier=instance_id)
            print(f"Instance {instance_id} stopped successfully")
        except Exception as e:
            print(f"Error stopping instance {instance_id}: {str(e)}")

    def delete_instance(self, instance_id, skip_final_snapshot=True):
        try:
            self.rds.delete_db_instance(
                DBInstanceIdentifier=instance_id,
                SkipFinalSnapshot=skip_final_snapshot
            )
            print(f"Instance {instance_id} deleted successfully")
        except Exception as e:
            print(f"Error deleting instance {instance_id}: {str(e)}")

    def delete_snapshot(self, snapshot_id):
        try:
            self.rds.delete_db_snapshot(DBSnapshotIdentifier=snapshot_id)
            print(f"Snapshot {snapshot_id} deleted successfully")
        except Exception as e:
            print(f"Error deleting snapshot {snapshot_id}: {str(e)}")

    def _can_delete_instance(self, tags):
        # Check if the instance has a tag that prevents deletion
        for tag in tags:
            if tag['Key'].lower() == 'retain' and tag['Value'].lower() == 'true':
                return False
        return True

    def _can_stop_instance(self, tags):
        # Check if the instance has a tag that prevents stopping
        for tag in tags:
            if tag['Key'].lower() == 'excludepower' and tag['Value'].lower() == 'true':
                return False
        return True

    def _is_older_snapshot(self, snapshot_date, days=2):
        # Check if the snapshot is older than specified days
        snapshot_date = datetime.strptime(snapshot_date, '%Y-%m-%d %H:%M:%S.%f')
        return (datetime.now() - snapshot_date) > timedelta(days=days)

    def cleanup_instances(self, status=None):
        instances = self.list_instances(status)
        for instance in instances:
            instance_id = instance['DBInstanceIdentifier']
            tags = instance.get('TagList', [])
            if self._can_delete_instance(tags):
                self.delete_instance(instance_id)
            elif self._can_stop_instance(tags) and instance['DBInstanceStatus'] == 'available':
                self.stop_instance(instance_id)

    def cleanup_snapshots(self, days=2):
        snapshots = self.list_snapshots()
        for snapshot in snapshots:
            snapshot_id = snapshot['DBSnapshotIdentifier']
            tags = snapshot.get('TagList', [])
            snapshot_date = snapshot['SnapshotCreateTime'].strftime('%Y-%m-%d %H:%M:%S.%f')
            if self._can_delete_instance(tags) and self._is_older_snapshot(snapshot_date, days):
                self.delete_snapshot(snapshot_id)

    def get_instance_status(self, instance_id):
        try:
            response = self.rds.describe_db_instances(DBInstanceIdentifier=instance_id)
            return response['DBInstances'][0]['DBInstanceStatus']
        except Exception as e:
            print(f"Error getting instance status: {str(e)}")

    def get_snapshot_status(self, snapshot_id):
        try:
            response = self.rds.describe_db_snapshots(DBSnapshotIdentifier=snapshot_id)
            return response['DBSnapshots'][0]['Status']
        except Exception as e:
            print(f"Error getting snapshot status: {str(e)}")

# Usage
rds_manager = RDSManager('us-east-1')
rds_manager.cleanup_instances()
rds_manager.cleanup_snapshots(days=7)