import pandas as pd

from src.data_gen import generate_data
from src.etl import build_analytics_tables


def test_etl_builds_tables(tmp_path):
    raw = tmp_path / "raw"
    processed = tmp_path / "processed"
    generate_data(output_dir=str(raw), n_users=40, n_products=15, start_date="2024-01-01", days=10, seed=123)
    build_analytics_tables(raw_dir=str(raw), out_dir=str(processed))
    assert (processed / "sessions.csv").exists()
    assert (processed / "orders_summary.csv").exists()
    assert (processed / "user_metrics.csv").exists()
