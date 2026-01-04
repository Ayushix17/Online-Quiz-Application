from pathlib import Path


def test_reports_dir_exists():
    p = Path("reports/figures")
    assert p.exists(), "reports/figures does not exist"


def test_at_least_one_figure():
    p = Path("reports/figures")
    files = list(p.glob("*"))
    # accept either PNG or HTML fallback
    assert any(f.suffix.lower() in ['.png', '.html'] for f in files), "No report figures found (png or html)"
