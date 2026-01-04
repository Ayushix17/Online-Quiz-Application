import pandas as pd
from pathlib import Path

raw = Path("data/raw")
out = Path("data/processed")
out.mkdir(parents=True, exist_ok=True)

# load raw tables
events = pd.read_csv(raw / "events.csv")
orders = pd.read_csv(raw / "orders.csv")
users = pd.read_csv(raw / "users.csv")

# normalize column names if necessary
if "event_type" not in events.columns:
    for c in ["event","type"]:
        if c in events.columns:
            events = events.rename(columns={c: "event_type"})
            break
if "session_id" not in events.columns:
    for c in ["session","sessionId"]:
        if c in events.columns:
            events = events.rename(columns={c: "session_id"})
            break
if "timestamp" not in events.columns:
    for c in ["time","ts","created_at"]:
        if c in events.columns:
            events = events.rename(columns={c: "timestamp"})
            break

# ensure channel and device columns exist; fallback to user_agent or 'unknown'
if "channel" not in events.columns:
    if "user_agent" in events.columns:
        events["channel"] = events["user_agent"]
    else:
        events["channel"] = "unknown"
if "device" not in events.columns:
    if "user_agent" in events.columns:
        events["device"] = events["user_agent"]
    else:
        events["device"] = "unknown"

session_info = events.groupby("session_id").agg(
    user_id=("user_id","first"),
    channel=("channel","first"),
    device=("device","first"),
    ts=("timestamp","min")
).reset_index()

# define helper to check event presence
def has_event(g, names):
    return g["event_type"].isin(names).any()

steps = {
    "view":["view","product_view","page_view","view_product"],
    "add_to_cart":["add_to_cart","cart"],
    "purchase":["purchase","order"]
}

sess_flags = events.groupby("session_id").apply(lambda g: pd.Series({
    "has_view": has_event(g, steps["view"]),
    "has_add": has_event(g, steps["add_to_cart"]),
    "has_purchase": has_event(g, steps["purchase"])
})).reset_index()

session_df = session_info.merge(sess_flags, on="session_id", how="left")

if "session_id" in orders.columns:
    purchased_sessions = orders["session_id"].dropna().unique()
    session_df.loc[session_df["session_id"].isin(purchased_sessions), "has_purchase"] = True

user_order_counts = orders.groupby("user_id").size().rename("order_count")
session_df = session_df.merge(user_order_counts, on="user_id", how="left").fillna({"order_count":0})
session_df["user_type"] = session_df["order_count"].apply(lambda x: "returning" if x>1 else "new")

# funnel counting helper
def funnel_counts(df):
    total_sessions = len(df)
    n_view = int(df["has_view"].sum())
    n_add = int(df["has_add"].sum())
    n_purchase = int(df["has_purchase"].sum())
    return pd.DataFrame({
        "step":["sessions","view","add_to_cart","purchase"],
        "count":[total_sessions, n_view, n_add, n_purchase]
    })

overall = funnel_counts(session_df)
by_channel = session_df.groupby("channel").apply(lambda g: funnel_counts(g).assign(channel=g.name)).reset_index(drop=True)
by_device = session_df.groupby("device").apply(lambda g: funnel_counts(g).assign(device=g.name)).reset_index(drop=True)
by_user_type = session_df.groupby("user_type").apply(lambda g: funnel_counts(g).assign(user_type=g.name)).reset_index(drop=True)

overall.to_csv(out / "funnel_overall.csv", index=False)
by_channel.to_csv(out / "funnel_by_channel.csv", index=False)
by_device.to_csv(out / "funnel_by_device.csv", index=False)
by_user_type.to_csv(out / "funnel_by_user_type.csv", index=False)
print("Wrote funnel summaries to data/processed/")