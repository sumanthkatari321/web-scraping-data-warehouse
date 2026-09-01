from __future__ import annotations
import pandas as pd
from .contracts import GOLD_COLUMNS, SILVER_COLUMNS


def to_silver(events: list[dict]) -> pd.DataFrame:
    frame = pd.DataFrame(events).copy()
    if frame.empty: return pd.DataFrame(columns=SILVER_COLUMNS)
    frame["event_ts"] = pd.to_datetime(frame["event_ts"], utc=True, errors="coerce")
    frame["quantity"] = pd.to_numeric(frame["quantity"], errors="coerce")
    frame["unit_price"] = pd.to_numeric(frame["unit_price"], errors="coerce")
    frame = frame.dropna(subset=["event_id", "order_id", "product_id", "event_ts", "quantity", "unit_price"])
    frame = frame[(frame.quantity > 0) & (frame.unit_price >= 0)].drop_duplicates(subset=["event_id"])
    frame["event_date"] = frame["event_ts"].dt.date.astype(str)
    frame["line_total"] = (frame["quantity"] * frame["unit_price"]).round(2)
    return frame[SILVER_COLUMNS].reset_index(drop=True)


def to_gold(silver: pd.DataFrame) -> pd.DataFrame:
    if silver.empty: return pd.DataFrame(columns=GOLD_COLUMNS)
    return (silver.groupby(["event_date", "product_id"], as_index=False).agg(orders=("order_id", "nunique"), units_sold=("quantity", "sum"), revenue=("line_total", "sum")).sort_values(["event_date", "product_id"])[GOLD_COLUMNS])


def validate_silver(frame: pd.DataFrame) -> None:
    if frame.empty: raise ValueError("No valid records available for silver publication")
    if frame.event_id.duplicated().any(): raise ValueError("Duplicate event IDs in silver layer")
    if (frame.line_total < 0).any(): raise ValueError("Negative line total in silver layer")
