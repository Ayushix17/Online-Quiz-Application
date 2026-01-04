"""Simple ETL to produce analytics-ready tables from raw CSVs.

Functions:
 - build_analytics_tables(raw_dir, out_dir)
"""
from __future__ import annotations

import os
import pandas as pd


def build_analytics_tables(raw_dir: str = "data/raw", out_dir: str = "data/processed") -> None:
    os.makedirs(out_dir, exist_ok=True)
    users = pd.read_csv(f"{raw_dir}/users.csv")
    products = pd.read_csv(f"{raw_dir}/products.csv")
    events = pd.read_csv(f"{raw_dir}/events.csv")
    orders = pd.read_csv(f"{raw_dir}/orders.csv")

    # sessions: count events per session
    sessions = (
        events.groupby(["session_id", "user_id"]).agg(
            events_count=("event_id", "count"),
            first_ts=("timestamp", "min"),
            last_ts=("timestamp", "max"),
        )
        .reset_index()
    )

    # orders summary
    if not orders.empty:
        orders_summary = (
            orders.groupby(["order_id", "user_id"]).agg(total=("total", "sum"), n_items=("quantity", "sum")).reset_index()
        )
    else:
        orders_summary = pd.DataFrame(columns=["order_id", "user_id", "total", "n_items"])

    # user metrics
    user_metrics = (
        orders_summary.groupby("user_id").agg(total_revenue=("total", "sum"), orders=("order_id", "nunique")).reset_index()
    )

    sessions.to_csv(f"{out_dir}/sessions.csv", index=False)
    orders_summary.to_csv(f"{out_dir}/orders_summary.csv", index=False)
    user_metrics.to_csv(f"{out_dir}/user_metrics.csv", index=False)

    print(f"Wrote analytics tables to {out_dir}")
