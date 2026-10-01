"""RDS manager: opt-in cleanup with final snapshots, pagination and tz-safe age checks."""
import logging
from datetime import datetime, timedelta, timezone

import boto3
from botocore.exceptions import ClientError

from .common import CleanupResult, is_eligible, default_dry_run

log = logging.getLogger(__name__)


class RDSManager:
    def __init__(self, region_name: str, dry_run: bool | None = None, client=None):
        self.region = region_name
        self.dry_run = default_dry_run() if dry_run is None else dry_run
        self.rds = client or boto3.client("rds", region_name=region_name)

    # ---------- listing (paginated) ----------
    def list_instances(self, status: str | None = None) -> list[dict]:
        out = []
        for page in self.rds.get_paginator("describe_db_instances").paginate():
            out += page["DBInstances"]
        return [i for i in out if status is None or i["DBInstanceStatus"] == status]

    def list_snapshots(self, snapshot_type: str = "manual") -> list[dict]:
        """Manual only: automated snapshots can't be deleted via delete_db_snapshot."""
        out = []
        for page in self.rds.get_paginator("describe_db_snapshots").paginate(SnapshotType=snapshot_type):
            out += page["DBSnapshots"]
        return out

    # ---------- status ----------
    def get_instance_status(self, instance_id: str) -> str:
        resp = self.rds.describe_db_instances(DBInstanceIdentifier=instance_id)
        return resp["DBInstances"][0]["DBInstanceStatus"]

    def get_snapshot_status(self, snapshot_id: str) -> str:
        resp = self.rds.describe_db_snapshots(DBSnapshotIdentifier=snapshot_id)
        return resp["DBSnapshots"][0]["Status"]

    # ---------- cleanup ----------
    def cleanup_instances(self, action: str = "stop") -> CleanupResult:
        """action='stop' (default, reversible) or 'delete' (takes a final snapshot)."""
        if action not in {"stop", "delete"}:
            raise ValueError("action must be 'stop' or 'delete'")
        result = CleanupResult()
        for inst in self.list_instances():
            iid = inst["DBInstanceIdentifier"]
            if not is_eligible(inst.get("TagList")):
                result.skipped.append(iid)
                continue
            if action == "stop":
                if inst["DBInstanceStatus"] != "available" or inst.get("ReadReplicaSourceDBInstanceIdentifier") \
                        or inst.get("ReadReplicaDBInstanceIdentifiers") or inst.get("DBClusterIdentifier"):
                    result.skipped.append(iid)   # cannot stop replicas, sources or Aurora members
                    continue
                self._act(result, iid, lambda i=iid: self.rds.stop_db_instance(DBInstanceIdentifier=i), "stop")
            else:
                stamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
                self._act(result, iid, lambda i=iid: self.rds.delete_db_instance(
                    DBInstanceIdentifier=i, SkipFinalSnapshot=False,
                    FinalDBSnapshotIdentifier=f"final-{i}-{stamp}",
                    DeleteAutomatedBackups=False), "delete")
        return result

    def cleanup_snapshots(self, days: int = 7) -> CleanupResult:
        result, cutoff = CleanupResult(), datetime.now(timezone.utc) - timedelta(days=days)
        for snap in self.list_snapshots():
            sid = snap["DBSnapshotIdentifier"]
            created = snap.get("SnapshotCreateTime")          # missing while 'creating'
            if created is None or created > cutoff or not is_eligible(snap.get("TagList")):
                result.skipped.append(sid)
                continue
            self._act(result, sid, lambda s=sid: self.rds.delete_db_snapshot(DBSnapshotIdentifier=s), "delete snapshot")
        return result

    def cleanup(self, action: str = "stop", snapshot_days: int = 7) -> CleanupResult:
        return self.cleanup_instances(action).merge(self.cleanup_snapshots(snapshot_days))

    def _act(self, result: CleanupResult, resource_id: str, fn, label: str) -> None:
        if self.dry_run:
            log.info("[DRY RUN] would %s %s", label, resource_id)
            result.acted.append(resource_id)
            return
        try:
            fn()
            log.info("Requested %s for %s (RDS completes this asynchronously)", label, resource_id)
            result.acted.append(resource_id)
        except ClientError as e:
            log.error("Failed to %s %s: %s", label, resource_id, e)
            result.errors.append({"id": resource_id, "error": str(e)})
