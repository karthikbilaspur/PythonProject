import boto3

from aws_ops.rds import RDSManager


def _db(rds, name, tags):
    rds.create_db_instance(DBInstanceIdentifier=name, DBInstanceClass="db.t3.micro", Engine="postgres",
                           MasterUsername="u", MasterUserPassword="password123", AllocatedStorage=20, Tags=tags)


def test_stop_only_opted_in(aws):
    rds = boto3.client("rds", region_name="us-east-1")
    _db(rds, "yes", [{"Key": "auto-cleanup", "Value": "true"}])
    _db(rds, "no", [])
    res = RDSManager("us-east-1", dry_run=False).cleanup_instances("stop")
    assert res.acted == ["yes"] and "no" in res.skipped
    assert RDSManager("us-east-1").get_instance_status("yes") == "stopped"
    assert RDSManager("us-east-1").get_instance_status("no") == "available"


def test_delete_takes_final_snapshot(aws):
    rds = boto3.client("rds", region_name="us-east-1")
    _db(rds, "gone", [{"Key": "auto-cleanup", "Value": "true"}])
    RDSManager("us-east-1", dry_run=False).cleanup_instances("delete")
    snaps = [s["DBSnapshotIdentifier"] for s in rds.describe_db_snapshots(SnapshotType="manual")["DBSnapshots"]]
    assert any(s.startswith("final-gone-") for s in snaps)


def test_dry_run_changes_nothing(aws):
    rds = boto3.client("rds", region_name="us-east-1")
    _db(rds, "keep", [{"Key": "auto-cleanup", "Value": "true"}])
    RDSManager("us-east-1", dry_run=True).cleanup_instances("delete")
    assert RDSManager("us-east-1").get_instance_status("keep") == "available"
