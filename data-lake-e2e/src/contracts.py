BRONZE_COLUMNS = ["event_id", "order_id", "product_id", "customer_id", "quantity", "unit_price", "event_ts"]
SILVER_COLUMNS = BRONZE_COLUMNS + ["event_date", "line_total"]
GOLD_COLUMNS = ["event_date", "product_id", "orders", "units_sold", "revenue"]
