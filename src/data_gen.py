from __future__ import annotations

"""Synthetic data generator for the Online Quiz Application analytics project.

This module produces realistic CSV datasets for users, products, events, and orders.

Usage:
    from src.data_gen import generate_data
    generate_data(output_dir="data/raw", n_users=500, n_products=100, start_date="2024-01-01", days=60)
"""

import os
import uuid
from datetime import datetime, timedelta
from collections import defaultdict

from faker import Faker
import numpy as np
import pandas as pd

fake = Faker()


def _make_dirs(output_dir: str) -> None:
    os.makedirs(output_dir, exist_ok=True)


def generate_products(n_products: int = 100) -> pd.DataFrame:
    categories = [
        "Electronics",
        "Home",
        "Clothing",
        "Sports",
        "Beauty",
        "Toys",
        "Books",
    ]
    rows = []
    for i in range(1, n_products + 1):
        price = round(float(np.random.lognormal(mean=3.0, sigma=0.8)), 2)
        rows.append(
            {
                "product_id": f"P{i:05d}",
                "category": np.random.choice(categories, p=[0.18, 0.18, 0.2, 0.12, 0.12, 0.1, 0.1]),
                "price": price,
                "title": fake.sentence(nb_words=3),
            }
        )
    return pd.DataFrame(rows)


def generate_users(n_users: int = 500, start_date: str = "2024-01-01", days: int = 60) -> pd.DataFrame:
    start = datetime.fromisoformat(start_date)
    channels = ["organic", "paid_search", "social", "email", "referral"]
    devices = ["desktop", "mobile", "tablet"]
    rows = []
    for i in range(1, n_users + 1):
        signup_offset = np.random.randint(0, days)
        signup_date = (start + timedelta(days=int(signup_offset))).date().isoformat()
        rows.append(
            {
                "user_id": f"U{i:06d}",
                "signup_date": signup_date,
                "channel": np.random.choice(channels, p=[0.45, 0.2, 0.15, 0.12, 0.08]),
                "device": np.random.choice(devices, p=[0.4, 0.55, 0.05]),
                "country": fake.country_code(),
            }
        )
    return pd.DataFrame(rows)


def generate_events(
    users: pd.DataFrame,
    products: pd.DataFrame,
    start_date: str = "2024-01-01",
    days: int = 60,
    seed: int | None = None,
) -> pd.DataFrame:
    if seed is not None:
        np.random.seed(seed)

    start = datetime.fromisoformat(start_date)
    event_rows = []
    order_rows = []

    product_ids = products["product_id"].tolist()
    product_price_map = products.set_index("product_id")["price"].to_dict()

    event_id = 0
    order_id = 0

    for _, u in users.iterrows():
        user_id = u["user_id"]
        # simulate sessions per user over the period
        avg_sessions = np.random.poisson(lam=3)
        n_sessions = max(1, avg_sessions)
        for s in range(n_sessions):
            # pick a random day and time
            day_offset = np.random.randint(0, days)
            session_start = start + timedelta(days=int(day_offset), seconds=int(np.random.randint(0, 86400)))
            session_id = str(uuid.uuid4())
            # page views
            n_views = np.random.randint(1, 6)
            viewed = np.random.choice(product_ids, size=n_views, replace=False)
            for pid in viewed:
                event_id += 1
                event_rows.append(
                    {
                        "event_id": f"E{event_id:08d}",
                        "event_type": "view_product",
                        "timestamp": session_start.isoformat(),
                        "user_id": user_id,
                        "session_id": session_id,
                        "product_id": pid,
                    }
                )

            # add to cart with some probability
            if np.random.rand() < 0.25:
                pid = np.random.choice(viewed)
                event_id += 1
                event_rows.append(
                    {
                        "event_id": f"E{event_id:08d}",
                        "event_type": "add_to_cart",
                        "timestamp": (session_start + timedelta(seconds=30)).isoformat(),
                        "user_id": user_id,
                        "session_id": session_id,
                        "product_id": pid,
                    }
                )

                # checkout with smaller probability
                if np.random.rand() < 0.4:
                    qty = int(np.random.choice([1, 1, 2, 3], p=[0.7, 0.1, 0.15, 0.05]))
                    order_id += 1
                    order_total = round(product_price_map[pid] * qty, 2)
                    order_rows.append(
                        {
                            "order_id": f"O{order_id:07d}",
                            "user_id": user_id,
                            "timestamp": (session_start + timedelta(minutes=5)).isoformat(),
                            "product_id": pid,
                            "quantity": qty,
                            "total": order_total,
                            "payment_success": np.random.rand() > 0.02,  # some payments fail
                        }
                    )
                    event_id += 1
                    event_rows.append(
                        {
                            "event_id": f"E{event_id:08d}",
                            "event_type": "purchase",
                            "timestamp": (session_start + timedelta(minutes=5)).isoformat(),
                            "user_id": user_id,
                            "session_id": session_id,
                            "product_id": pid,
                        }
                    )

    events = pd.DataFrame(event_rows)
    orders = pd.DataFrame(order_rows)
    return events, orders


def generate_data(output_dir: str = "data/raw", n_users: int = 500, n_products: int = 100, start_date: str = "2024-01-01", days: int = 60, seed: int | None = None) -> None:
    """Generate synthetic CSV datasets and save to output_dir.

    Produces: users.csv, products.csv, events.csv, orders.csv
    """
    _make_dirs(output_dir)
    users = generate_users(n_users=n_users, start_date=start_date, days=days)
    products = generate_products(n_products)
    events, orders = generate_events(users, products, start_date=start_date, days=days, seed=seed)

    users.to_csv(os.path.join(output_dir, "users.csv"), index=False)
    products.to_csv(os.path.join(output_dir, "products.csv"), index=False)
    events.to_csv(os.path.join(output_dir, "events.csv"), index=False)
    orders.to_csv(os.path.join(output_dir, "orders.csv"), index=False)

    print(f"Wrote: {output_dir}/users.csv ({len(users)} rows)")
    print(f"Wrote: {output_dir}/products.csv ({len(products)} rows)")
    print(f"Wrote: {output_dir}/events.csv ({len(events)} rows)")
    print(f"Wrote: {output_dir}/orders.csv ({len(orders)} rows)")
    print(f"Wrote: {output_dir}/orders.csv ({len(orders)} rows)")
