from __future__ import annotations
import argparse
import io
import uuid
from datetime import UTC, datetime
from .generate import retail_events
from .lake import bucket, put_bytes, put_json, write_bronze
from .transform import to_gold, to_silver, validate_silver


def write_parquet(frame, layer: str, run_id: str) -> str:
    buffer = io.BytesIO(); frame.to_parquet(buffer, index=False)
    prefix = f"{layer}/retail_orders/published_date={datetime.now(UTC):%Y-%m-%d}/run_id={run_id}"
    put_bytes(f"{prefix}/part-00000.parquet", buffer.getvalue(), "application/octet-stream")
    put_json(f"{prefix}/_SUCCESS.json", {"run_id": run_id, "row_count": len(frame), "published_at": datetime.now(UTC).isoformat()})
    return prefix


def run(records: int) -> dict[str, str]:
    run_id = str(uuid.uuid4()); events = retail_events(records); bronze = write_bronze(events, run_id)
    silver = to_silver(events); validate_silver(silver)
    return {"bucket": bucket(), "bronze": bronze, "silver": write_parquet(silver, "silver", run_id), "gold": write_parquet(to_gold(silver), "gold", run_id)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the LakeFlow retail lake pipeline")
    parser.add_argument("--records", type=int, default=1_000)
    print(run(parser.parse_args().records))
