from src.transform import to_gold, to_silver, validate_silver


def test_silver_removes_invalid_and_duplicate_events():
    events = [
        {"event_id": "a", "order_id": "o1", "product_id": "p1", "customer_id": "c1", "quantity": 2, "unit_price": 10, "event_ts": "2026-01-01T00:00:00Z"},
        {"event_id": "a", "order_id": "o1", "product_id": "p1", "customer_id": "c1", "quantity": 2, "unit_price": 10, "event_ts": "2026-01-01T00:00:00Z"},
        {"event_id": "bad", "order_id": "o2", "product_id": "p2", "customer_id": "c2", "quantity": 0, "unit_price": 5, "event_ts": "2026-01-01T00:00:00Z"},
    ]
    silver = to_silver(events); validate_silver(silver)
    assert len(silver) == 1 and silver.iloc[0].line_total == 20


def test_gold_aggregates_order_metrics():
    silver = to_silver([
        {"event_id": "a", "order_id": "o1", "product_id": "p1", "customer_id": "c1", "quantity": 2, "unit_price": 10, "event_ts": "2026-01-01T00:00:00Z"},
        {"event_id": "b", "order_id": "o1", "product_id": "p1", "customer_id": "c1", "quantity": 3, "unit_price": 10, "event_ts": "2026-01-01T01:00:00Z"},
    ])
    gold = to_gold(silver)
    assert gold.iloc[0].orders == 1 and gold.iloc[0].units_sold == 5 and gold.iloc[0].revenue == 50
