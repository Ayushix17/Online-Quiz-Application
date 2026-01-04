import pandas as pd
from pathlib import Path


def test_funnel_files_exist():
    base = Path("data/processed")
    for fn in ["funnel_overall.csv","funnel_by_channel.csv","funnel_by_device.csv","funnel_by_user_type.csv"]:
        assert (base / fn).exists(), f"Missing funnel summary: {fn}"


def test_funnel_counts_nonincreasing():
    df = pd.read_csv("data/processed/funnel_overall.csv")
    counts = df["count"].tolist()
    # expect: sessions >= view >= add_to_cart >= purchase
    assert len(counts) >= 4, "Unexpected funnel shape"
    assert counts[0] >= counts[1] >= counts[2] >= counts[3], "Funnel counts should be non-increasing"
