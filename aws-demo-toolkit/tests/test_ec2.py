import boto3
import pytest

from aws_ops.ec2 import EC2Manager

TAG = [{"Key": "auto-cleanup", "Value": "true"}]


def _volume(ec2, tags):
    kw = {"TagSpecifications": [{"ResourceType": "volume", "Tags": tags}]} if tags else {}
    return ec2.create_volume(AvailabilityZone="us-east-1a", Size=1, **kw)["VolumeId"]


def test_only_opted_in_volumes_deleted(aws):
    ec2 = boto3.client("ec2", region_name="us-east-1")
    tagged, untagged = _volume(ec2, TAG), _volume(ec2, None)
    retained = _volume(ec2, TAG + [{"Key": "retain", "Value": "true"}])
    res = EC2Manager("us-east-1", dry_run=False).delete_available_volumes()
    assert res.acted == [tagged]
    remaining = {v["VolumeId"] for v in ec2.describe_volumes()["Volumes"]}
    assert untagged in remaining and retained in remaining and tagged not in remaining


def test_dry_run_deletes_nothing(aws):
    ec2 = boto3.client("ec2", region_name="us-east-1")
    vid = _volume(ec2, TAG)
    res = EC2Manager("us-east-1", dry_run=True).delete_available_volumes()
    assert res.acted == [vid]
    assert len(ec2.describe_volumes()["Volumes"]) == 1


def test_old_tagged_snapshot_deleted(aws):
    ec2 = boto3.client("ec2", region_name="us-east-1")
    vid = _volume(ec2, None)
    snap = ec2.create_snapshot(VolumeId=vid, TagSpecifications=[{"ResourceType": "snapshot", "Tags": TAG}])["SnapshotId"]
    res = EC2Manager("us-east-1", dry_run=False).delete_old_snapshots(days=0)
    assert snap in res.acted


def test_create_instances_validates_count(aws):
    with pytest.raises(ValueError):
        EC2Manager("us-east-1").create_instances("ami-x", 0)
