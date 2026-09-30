"""EC2 helpers: creation utilities and safe, opt-in cleanup."""
import logging
import uuid
from datetime import datetime, timedelta, timezone

import boto3
from botocore.exceptions import ClientError

from .common import CleanupResult, OPT_IN_TAG, is_eligible, default_dry_run

log = logging.getLogger(__name__)


class EC2Manager:
    def __init__(self, region_name: str, dry_run: bool | None = None, client=None):
        self.region = region_name
        self.dry_run = default_dry_run() if dry_run is None else dry_run
        self.ec2 = client or boto3.client("ec2", region_name=region_name)

    # ---------- creation (errors propagate; caller decides what to do) ----------
    def create_instances(self, ami_id: str, count: int = 1, instance_type: str = "t3.micro",
                         tags: dict | None = None) -> list[str]:
        if count < 1:
            raise ValueError("count must be >= 1")
        tag_list = [{"Key": k, "Value": v} for k, v in (tags or {}).items()]
        resp = self.ec2.run_instances(
            ImageId=ami_id, InstanceType=instance_type, MinCount=count, MaxCount=count,
            ClientToken=str(uuid.uuid4()),  # idempotency: safe to retry
            TagSpecifications=[{"ResourceType": "instance", "Tags": tag_list}] if tag_list else [],
        )
        ids = [i["InstanceId"] for i in resp["Instances"]]
        log.info("Created %d instances: %s", count, ids)
        return ids

    def create_volume(self, availability_zone: str, size: int = 10, volume_type: str = "gp3",
                      encrypted: bool = True) -> str:
        resp = self.ec2.create_volume(AvailabilityZone=availability_zone, Size=size,
                                      VolumeType=volume_type, Encrypted=encrypted)
        log.info("Created volume %s in %s", resp["VolumeId"], availability_zone)
        return resp["VolumeId"]

    def create_snapshot(self, volume_id: str, description: str = "") -> str:
        resp = self.ec2.create_snapshot(VolumeId=volume_id, Description=description)
        log.info("Created snapshot %s for %s", resp["SnapshotId"], volume_id)
        return resp["SnapshotId"]

    def create_vpc(self, cidr_block: str) -> str:
        resp = self.ec2.create_vpc(CidrBlock=cidr_block)
        vpc_id = resp["Vpc"]["VpcId"]
        log.info("Created VPC %s (%s)", vpc_id, cidr_block)
        return vpc_id

    # ---------- cleanup ----------
    def _ami_snapshot_ids(self) -> set[str]:
        """Snapshots that back an AMI cannot be deleted; collect them to skip."""
        ids = set()
        for page in self.ec2.get_paginator("describe_images").paginate(Owners=["self"]):
            for image in page["Images"]:
                for bdm in image.get("BlockDeviceMappings", []):
                    if "Ebs" in bdm and "SnapshotId" in bdm["Ebs"]:
                        ids.add(bdm["Ebs"]["SnapshotId"])
        return ids

    def delete_old_snapshots(self, days: int) -> CleanupResult:
        result, cutoff = CleanupResult(), datetime.now(timezone.utc) - timedelta(days=days)
        protected = self._ami_snapshot_ids()
        pages = self.ec2.get_paginator("describe_snapshots").paginate(OwnerIds=["self"])
        for page in pages:
            for snap in page["Snapshots"]:
                sid = snap["SnapshotId"]
                if (not is_eligible(snap.get("Tags")) or sid in protected
                        or snap["StartTime"] > cutoff):
                    result.skipped.append(sid)
                    continue
                self._act(result, sid, lambda s=sid: self.ec2.delete_snapshot(SnapshotId=s), "delete snapshot")
        return result

    def delete_available_volumes(self) -> CleanupResult:
        result = CleanupResult()
        pages = self.ec2.get_paginator("describe_volumes").paginate(
            Filters=[{"Name": "status", "Values": ["available"]},
                     {"Name": f"tag:{OPT_IN_TAG}", "Values": ["true"]}])
        for page in pages:
            for vol in page["Volumes"]:
                vid = vol["VolumeId"]
                if not is_eligible(vol.get("Tags")):
                    result.skipped.append(vid)
                    continue
                self._act(result, vid, lambda v=vid: self.ec2.delete_volume(VolumeId=v), "delete volume")
        return result

    def stop_instances(self) -> CleanupResult:
        result = CleanupResult()
        pages = self.ec2.get_paginator("describe_instances").paginate(
            Filters=[{"Name": "instance-state-name", "Values": ["running"]},
                     {"Name": f"tag:{OPT_IN_TAG}", "Values": ["true"]}])
        for page in pages:
            for reservation in page["Reservations"]:
                for inst in reservation["Instances"]:
                    iid = inst["InstanceId"]
                    if not is_eligible(inst.get("Tags")):
                        result.skipped.append(iid)
                        continue
                    self._act(result, iid, lambda i=iid: self.ec2.stop_instances(InstanceIds=[i]), "stop instance")
        return result

    def _act(self, result: CleanupResult, resource_id: str, fn, label: str) -> None:
        if self.dry_run:
            log.info("[DRY RUN] would %s %s", label, resource_id)
            result.acted.append(resource_id)
            return
        try:
            fn()
            log.info("Did %s %s", label, resource_id)
            result.acted.append(resource_id)
        except ClientError as e:
            log.error("Failed to %s %s: %s", label, resource_id, e)
            result.errors.append({"id": resource_id, "error": str(e)})

    def cleanup(self, snapshot_days: int = 7) -> CleanupResult:
        result = CleanupResult()
        for step in (lambda: self.delete_old_snapshots(snapshot_days),
                     self.delete_available_volumes, self.stop_instances):
            result.merge(step())
        return result
