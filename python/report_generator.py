import argparse
import csv
from datetime import datetime
from pathlib import Path

from kpi_engine import (
    load_data,
    total_content,
    total_views,
    total_engagement,
    engagement_rate,
    top_platform,
    top_content_type,
    average_views_per_post,
    average_engagement_per_post,
    platform_breakdown,
    platform_engagement_rate,
    content_type_breakdown,
)


# ~ Terminal Report
# --------------------------------------------------
# Generate a formatted KPI report for terminal output.

def print_report(df):
    """Print KPI summary to the terminal."""

    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    print("\n" + "=" * 50)
    print("Social Media KPI REPORT")
    print(f"Generated: {now}")
    print("=" * 50)

    print(f"Total Content: {total_content(df):>10,}")
    print(f"Total Views: {total_views(df):>10,}")
    print(f"Total Engagement: {total_engagement(df):>10,}")
    print(f"Engagement Rate: {engagement_rate(df):>10.2%}")
    print(f"Avg Views / Post: {average_views_per_post(df):>10,.0f}")
    print(f"Avg Engagement / Post: {average_engagement_per_post(df):>10,.0f}")

    print()
    print(f"Top Platform: {top_platform(df)}")
    print(f"Top Content Type: {top_content_type(df)}")

    print("\n" + "=" * 50)
    print("Breakdowns by platform")
    print("=" * 50)
    print(platform_breakdown(df).to_string())

    print("\n" + "=" * 50)
    print("Engagement rates by platform")
    print("=" * 50)

    eng = platform_engagement_rate(df)[["engagement_rate"]].copy()
    eng["engagement_rate"] = eng["engagement_rate"].map("{:.2%}".format)

    print(eng.to_string())

    print("\n" + "=" * 50)
    print("Content type breakdown")
    print("=" * 50)
    print(content_type_breakdown(df).to_string())
    print()


# ~ CSV Export
# --------------------------------------------------
# Export top-level KPIs to CSV.

def export_csv(df, output_path: str):
    """Export KPI summary to CSV."""

    out = Path(output_path)

    # Create output directories if needed.
    out.parent.mkdir(parents=True, exist_ok=True)

    rows = [
        ("metric", "value"),
        ("generated_at", datetime.now().isoformat()),
        ("total_content", total_content(df)),
        ("total_views", total_views(df)),
        ("total_engagement", total_engagement(df)),
        ("engagement_rate", f"{engagement_rate(df):.4f}"),
        ("avg_views_per_post", f"{average_views_per_post(df):.2f}"),
        ("avg_engagement_per_post", f"{average_engagement_per_post(df):.2f}"),
        ("top_platform", top_platform(df)),
        ("top_content_type", top_content_type(df)),
    ]

    with open(out, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    print(f"CSV report saved to: {out}")



 
# Load data, print report, and optionally export CSV.
# --------------------------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate Civic Media KPI report."
    )

    parser.add_argument(
        "--csv",
        metavar="OUTPUT_PATH",
        help="Export KPI summary to CSV."
    )

    args = parser.parse_args()

    df = load_data()

    print_report(df)

    if args.csv:
        export_csv(df, args.csv)