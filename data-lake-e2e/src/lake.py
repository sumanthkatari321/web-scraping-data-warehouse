from __future__ import annotations

import hashlib
import json
import os
from datetime import UTC, datetime
import boto3


def client():
    return boto3.client("s3", endpoint_url=os.environ.get("S3_ENDPOINT", "http://localhost:9000"), aws_access_key_id=os.environ.get("S3_ACCESS_KEY", "minioadmin"), aws_secret_access_key=os.environ.get("S3_SECRET_KEY", "minioadmin"))


def bucket() -> str: return os.environ.get("LAKE_BUCKET", "lake")


def put_bytes(key: str, payload: bytes, content_type: str) -> None:
    client().put_object(Bucket=bucket(), Key=key, Body=payload, ContentType=content_type)


def put_json(key: str, value: object) -> None:
    put_bytes(key, json.dumps(value, default=str, indent=2).encode(), "application/json")


def write_bronze(events: list[dict], run_id: str) -> str:
    prefix = f"bronze/retail_orders/ingest_date={datetime.now(UTC):%Y-%m-%d}/run_id={run_id}"
    payload = "\n".join(json.dumps(event) for event in events).encode()
    put_bytes(f"{prefix}/events.jsonl", payload, "application/x-ndjson")
    put_json(f"{prefix}/manifest.json", {"run_id": run_id, "record_count": len(events), "schema_version": 1, "sha256": hashlib.sha256(payload).hexdigest(), "landed_at": datetime.now(UTC).isoformat()})
    return prefix
