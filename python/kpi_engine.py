from pathlib import Path
import pandas as pd

# ~ Path Setup

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent

DATA_PATH = (PROJECT_ROOT / "testing" / "data" / "social_media_metrics.csv")

# ~ Data Loading

def load_data():
    """Load social media metrics dataset."""
    return pd.read_csv(DATA_PATH)


# ~ Core KPI Metrics

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
    """Calculate total engagement interactions."""
    return (
        total_likes(df)
        + total_shares(df)
        + total_comments(df)
    )


def engagement_rate(df):
    """Calculate engagement relative to views."""
    views = total_views(df)

    if views == 0:
        return 0

    return total_engagement(df) / views


# ~ Breakdowns

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

def top_platform(df):
    """Identify the platform with the most views."""
    return (
        df.groupby("platform")["views"]
        .sum()
        .idxmax()
    )


def top_content_type(df):
    """Identify the content type with the most views."""
    return (
        df.groupby("content_type")["views"]
        .sum()
        .idxmax()
    )


# ~ Additional Metrics

def average_views_per_post(df):
    """Calculate average views per post."""
    return df["views"].mean()


def average_engagement_per_post(df):
    """Calculate average engagement per post."""
    return (
        df["likes"] +
        df["shares"] +
        df["comments"]
    ).mean()


def platform_engagement_rate(df):
    """Calculate engagement rate by platform."""
    grouped = (
        df.groupby("platform")
        .agg({
            "views": "sum",
            "likes": "sum",
            "shares": "sum",
            "comments": "sum"
        })
    )

    grouped["engagement_rate"] = (
        grouped["likes"] +
        grouped["shares"] +
        grouped["comments"]
    ) / grouped["views"]

    return grouped.sort_values(
        "engagement_rate",
        ascending=False
    )


# ~ Reporting

def print_report(df):

    print("\n" + "=" * 50)
    print("CIVIC MEDIA KPI REPORT")
    print("=" * 50)

    print(f"Total Content:     {total_content(df):,}")
    print(f"Total Views:       {total_views(df):,}")
    print(f"Total Engagement:  {total_engagement(df):,}")
    print(f"Engagement Rate:   {engagement_rate(df):.2%}")

    print(f"Top Platform:      {top_platform(df)}")
    print(f"Top Content Type:  {top_content_type(df)}")

    print("\n" + "=" * 50)
    print("PLATFORM BREAKDOWN")
    print("=" * 50)

    print(platform_breakdown(df))


# ~ Run Script

if __name__ == "__main__":

    df = load_data()

    print_report(df)