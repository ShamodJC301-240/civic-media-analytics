from pathlib import Path
import os
import pandas as pd

# ~ Path Setup
# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent

DEFAULT_DATA_PATH = PROJECT_ROOT / "testing" / "data" / "social_media_metrics.csv"
DATA_PATH = Path(os.environ.get("METRICS_CSV", DEFAULT_DATA_PATH))

# ~ Required columns for KPI calculations
# ----------------------------------------------
REQUIRED_COLUMNS = {
    "views", "likes", "shares",
    "comments", "platform", "content_type"
}


# ~ Data Loading
# --------------------------------------------------

def load_data(path=DATA_PATH):
    """Load social media metrics dataset.

    Args:
        path: Path to CSV file.

    Raises:
        FileNotFoundError: CSV does not exist.
        ValueError: Required columns are missing.
    """

    # Give a clear error if the file cannot be found.
    if not Path(path).exists():
        raise FileNotFoundError(
            f"Metrics CSV not found at: {path}\n"
            "Set the METRICS_CSV environment variable or check your path."
        )

    df = pd.read_csv(path)

    # Validate columns before any KPI calculations run.
    _validate_columns(df)

    return df


def _validate_columns(df):
    """Ensure all required columns exist."""

    missing = REQUIRED_COLUMNS - set(df.columns)

    if missing:
        raise ValueError(
            f"CSV is missing required columns: {missing}\n"
            f"Found columns: {list(df.columns)}"
        )


# ~ Core Metrics
# --------------------------------------------------

def total_content(df):
    """Count total content records."""
    return len(df)

def total_views(df):
    """Calculate total views."""
    return df["views"].sum()

def total_likes(df):
    """Calculate total likes."""
    return df["likes"].sum()

def total_shares(df):
    """Calculate total shares."""
    return df["shares"].sum()

def total_comments(df):
    """Calculate total comments."""
    return df["comments"].sum()

def total_engagement(df):
    """Calculate total engagement."""

    return (
        total_likes(df)
        + total_shares(df)
        + total_comments(df)
    )

def engagement_rate(df):
    """Calculate overall engagement rate."""

    views = total_views(df)

    # Prevent division by zero.
    if views == 0:
        return 0

    return total_engagement(df) / views


# Breakdowns
# --------------------------------------------------

def platform_breakdown(df):
    """Summarize metrics by platform."""

    return (
        df.groupby("platform")[
            ["views", "likes", "shares", "comments"]
        ]
        .sum()
        .sort_values("views", ascending=False)
    )


def content_type_breakdown(df):
    """Summarize metrics by content type."""

    return (
        df.groupby("content_type")[
            ["views", "likes", "shares", "comments"]
        ]
        .sum()
        .sort_values("views", ascending=False)
    )


# ~ Top Performers
# --------------------------------------------------

def top_platform(df):
    """Return platform with highest total views."""

    return (
        df.groupby("platform")["views"]
        .sum()
        .idxmax()
    )


def top_content_type(df):
    """Return content type with highest total views."""

    return (
        df.groupby("content_type")["views"]
        .sum()
        .idxmax()
    )


# ~ Additional Metrics
# --------------------------------------------------

def average_views_per_post(df):
    """Calculate average views per post."""
    return df["views"].mean()


def average_engagement_per_post(df):
    """Calculate average engagement per post."""

    return (
        df["likes"]
        + df["shares"]
        + df["comments"]
    ).mean()


def platform_engagement_rate(df):
    """Calculate engagement rate by platform."""

    grouped = df.groupby("platform").agg({
        "views": "sum",
        "likes": "sum",
        "shares": "sum",
        "comments": "sum",
    })

    # ~ Avoid division by zero for platforms with no views.
    # --------------------------------------------------------
    grouped["engagement_rate"] = (
        (grouped["likes"] + grouped["shares"] + grouped["comments"])
        / grouped["views"].replace(0, float("nan"))
    )

    return grouped.sort_values(
        "engagement_rate",
        ascending=False
    )


# ~ Load data and print report
if __name__ == "__main__":
    from report_generator import print_report, export_csv

    df = load_data()

    print_report(df)