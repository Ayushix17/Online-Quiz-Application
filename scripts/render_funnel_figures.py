"""Render funnel figures to reports/figures as PNG (preferred) with HTML fallback.

Usage: python scripts/render_funnel_figures.py
"""
from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.io as pio

raw = Path("data/raw")
processed = Path("data/processed")
out = Path("reports/figures")
out.mkdir(parents=True, exist_ok=True)

# read processed funnel files
overall = pd.read_csv(processed / "funnel_overall.csv")
by_channel = pd.read_csv(processed / "funnel_by_channel.csv") if (processed / "funnel_by_channel.csv").exists() else None

# helper to export figure with PNG preferred and HTML fallback

def export_fig(fig, out_path_base: Path):
    png_path = out_path_base.with_suffix('.png')
    html_path = out_path_base.with_suffix('.html')
    try:
        # Try to write PNG using kaleido
        fig.write_image(str(png_path))
        print(f"Wrote: {png_path}")
        return png_path
    except Exception as e:
        try:
            fig.write_html(str(html_path))
            print(f"PNG export failed ({e}); wrote HTML: {html_path}")
            return html_path
        except Exception as e2:
            print(f"Failed to export figure: {e2}")
            return None

# overall funnel
try:
    fig = px.funnel(overall, x='count', y='step', title='Overall Funnel')
    export_fig(fig, out / 'funnel_overall')
except Exception as e:
    print('Failed to create overall funnel plot:', e)

# per-channel funnels (top 5 channels by sessions)
if by_channel is not None and not by_channel.empty:
    channel_counts = by_channel[by_channel['step']=='sessions'].sort_values('count', ascending=False)
    top_channels = channel_counts['channel'].head(5).tolist()
    for ch in top_channels:
        df = by_channel[by_channel['channel']==ch]
        if df.empty:
            continue
        try:
            fig = px.funnel(df, x='count', y='step', title=f'Funnel - {ch}')
            safe_name = ''.join(c if c.isalnum() else '_' for c in ch)[:50]
            export_fig(fig, out / f'funnel_channel_{safe_name}')
        except Exception as e:
            print(f'Failed to create funnel for channel {ch}:', e)

print('Report generation completed.')
