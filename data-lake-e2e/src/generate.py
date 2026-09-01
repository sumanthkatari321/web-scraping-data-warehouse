from __future__ import annotations

import random
import uuid
from datetime import UTC, datetime, timedelta


def retail_events(records: int, seed: int = 42) -> list[dict]:
    """Produce deterministic synthetic retail order-line events."""
    randomizer = random.Random(seed)
    now = datetime.now(UTC)
    return [{
        "event_id": str(uuid.uuid4()), "order_id": f"ORD-{randomizer.randint(100000, 999999)}",
        "product_id": f"SKU-{randomizer.randint(1, 50):03d}", "customer_id": f"CUS-{randomizer.randint(1, 500):04d}",
        "quantity": randomizer.randint(1, 5), "unit_price": round(randomizer.uniform(5, 250), 2),
        "event_ts": (now - timedelta(minutes=randomizer.randint(0, 60 * 24 * 14))).isoformat(),
    } for _ in range(records)]
