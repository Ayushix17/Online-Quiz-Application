import os
import shutil

from src.data_gen import generate_data


def test_generate_data(tmp_path):
    out = tmp_path / "raw"
    generate_data(output_dir=str(out), n_users=50, n_products=20, start_date="2024-01-01", days=14, seed=42)
    assert (out / "users.csv").exists()
    assert (out / "products.csv").exists()
    assert (out / "events.csv").exists()
    assert (out / "orders.csv").exists()
