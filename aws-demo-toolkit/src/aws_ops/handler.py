"""AWS Lambda entrypoint: runs EC2 + RDS cleanup across enabled regions."""
import json
import logging
import os

import boto3
from botocore.exceptions import ClientError

from .common import CleanupResult, default_dry_run
from .ec2 import EC2Manager
from .rds import RDSManager

log = logging.getLogger(__name__)
MIN_REMAINING_MS = 60_000   # stop starting new regions when < 60s remain


def enabled_regions() -> list[str]:
    ec2 = boto3.client("ec2")
    resp = ec2.describe_regions(Filters=[{"Name": "opt-in-status",
                                          "Values": ["opt-in-not-required", "opted-in"]}])
    return [r["RegionName"] for r in resp["Regions"]]


def lambda_handler(event, context):
    dry_run = default_dry_run()
    snapshot_days = int(os.getenv("SNAPSHOT_DAYS", "7"))
    rds_action = os.getenv("RDS_ACTION", "stop")
    log.info("Starting cleanup (dry_run=%s, snapshot_days=%s, rds_action=%s)",
             dry_run, snapshot_days, rds_action)

    try:
        regions = enabled_regions()
    except ClientError as e:
        log.error("Failed to describe regions: %s", e)
        return {"statusCode": 500, "body": json.dumps({"error": "failed to describe regions"})}

    report, failed, unprocessed = {}, [], []
    for i, region in enumerate(regions):
        if context is not None and context.get_remaining_time_in_millis() < MIN_REMAINING_MS:
            unprocessed = regions[i:]
            log.warning("Low on time; not processed: %s", unprocessed)
            break
        try:
            result = CleanupResult()
            result.merge(EC2Manager(region, dry_run).cleanup(snapshot_days))
            result.merge(RDSManager(region, dry_run).cleanup(rds_action, snapshot_days))
            report[region] = result.to_dict()
            if result.errors:
                failed.append(region)
        except Exception:   # one bad region must not abort the rest
            log.exception("Region %s failed", region)
            failed.append(region)

    body = {"dry_run": dry_run, "report": report, "failed_regions": failed, "unprocessed_regions": unprocessed}
    return {"statusCode": 200 if not failed and not unprocessed else 500, "body": json.dumps(body, default=str)}
