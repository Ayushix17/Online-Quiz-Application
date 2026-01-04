import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(layout="wide", page_title="E-commerce Growth Analysis (Demo)")
st.title("E-commerce Growth Analysis — Demo Dashboard")

DATA_DIR = Path("data/raw")

@st.cache_data
def load_data():
    products = pd.read_csv(DATA_DIR / "products.csv")
    users = pd.read_csv(DATA_DIR / "users.csv")
    sessions = pd.read_csv(DATA_DIR / "sessions.csv")
    events = pd.read_csv(DATA_DIR / "events.csv")
    orders = pd.read_csv(DATA_DIR / "orders.csv") if (DATA_DIR / "orders.csv").exists() else pd.DataFrame()
    return products, users, sessions, events, orders

st.sidebar.header("Controls")
if st.sidebar.button("Reload data"):
    st.cache_data.clear()

products, users, sessions, events, orders = load_data()

st.header("Quick KPIs")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Users", int(users.shape[0]))
with col2:
    st.metric("Sessions", int(sessions.shape[0]))
with col3:
    st.metric("Events", int(events.shape[0]))
with col4:
    st.metric("Orders", int(orders.shape[0]))

st.header("Top categories by revenue (sample)")
if not orders.empty:
    # simple join from orders -> order_items would be needed for real revenue
    st.write(orders.head())
else:
    st.write("No orders found yet. Generate data first using the data generator.")

st.header("Event sample")
st.dataframe(events.sample(min(100, len(events))))
