# AWS Ops Toolkit

One project combining EC2/RDS cleanup (Lambda) and an SQS service with a Flask API.

```
src/aws_ops/
  common.py   settings, opt-in tag logic, CleanupResult
  ec2.py      EC2Manager  (create + safe cleanup)
  rds.py      RDSManager  (stop/delete with final snapshot)
  sqs.py      SQSService  (stateless, real AWS; mocking lives in tests)
  api.py      Flask app factory (API key auth, validation, status codes)
  handler.py  Lambda entrypoint
tests/        moto-based tests
```

## Safety model
- **Dry-run by default.** Set `DRY_RUN=false` to actually change anything.
- **Opt-in:** only resources tagged `auto-cleanup=true` are touched; `retain=true` always wins.
- RDS: default action is **stop**; `RDS_ACTION=delete` takes a final snapshot and keeps automated backups.
- EC2 snapshots that back an AMI are never deleted.

## Config (env vars)
`DRY_RUN` (true), `SNAPSHOT_DAYS` (7), `RDS_ACTION` (stop), `API_KEY` (required for API), `AWS_REGION`, `LOG_LEVEL`.

## Run
```
pip install -r requirements-dev.txt && pytest
API_KEY=changeme python -m aws_ops.api      # dev server
```
Lambda handler: `aws_ops.handler.lambda_handler`. Needs IAM for ec2/rds Describe/Delete/Stop and `ec2:DescribeRegions`.
