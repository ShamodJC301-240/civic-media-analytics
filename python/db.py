# Database connection, schema, and data access.
# All modules import from here.

import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load .env for testing
load_dotenv()


# ~ Connection
# --------------------------------------------------

def get_engine():
    """Create SQLAlchemy engine from env vars."""

    required = ["DB_USER", "DB_PASS", "DB_HOST", "DB_NAME"]

    # Fail fast if config is missing.
    missing = [v for v in required if not os.environ.get(v)]

    if missing:
        raise EnvironmentError(
            f"Missing environment variables: {missing}\n"
            "Add them to .env or system env."
        )

    user     = os.environ["DB_USER"]
    password = os.environ["DB_PASS"]
    host     = os.environ["DB_HOST"]
    port     = os.environ.get("DB_PORT", "5432")
    name     = os.environ["DB_NAME"]

    return create_engine(
        f"postgresql://{user}:{password}@{host}:{port}/{name}"
    )


# ~ Schema. Keeping it in sync with other loaders
# --------------------------------------------------

_CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS media_events (
    id              SERIAL PRIMARY KEY,
    platform        TEXT        NOT NULL,
    content_type    TEXT        NOT NULL,
    views           BIGINT      NOT NULL DEFAULT 0,
    likes           BIGINT      NOT NULL DEFAULT 0,
    shares          BIGINT      NOT NULL DEFAULT 0,
    comments        BIGINT      NOT NULL DEFAULT 0,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
"""


def create_schema(engine=None):
    """Create media_events table if it doesn't exist."""

    engine = engine or get_engine()

    with engine.begin() as conn:
        conn.execute(text(_CREATE_TABLE_SQL))

    print("Schema ready: media_events exists.")


# ~ Data Access
# --------------------------------------------------

def fetch_data(engine=None, where: str = None):
    """Fetch raw media_events as a DataFrame."""

    engine = engine or get_engine()

    query = "SELECT * FROM media_events"

    if where:
        query += f" WHERE {where}"

    df = pd.read_sql(query, engine)

    if df.empty:
        raise ValueError(
            "No data found in media_events.\n"
            "Load data first using load_postgres.py."
        )

    return df


def fetch_platform_summary(engine=None):
    """Get aggregated metrics by platform."""

    engine = engine or get_engine()

    query = """
        SELECT
            platform,
            SUM(views)    AS views,
            SUM(likes)    AS likes,
            SUM(shares)   AS shares,
            SUM(comments) AS comments
        FROM media_events
        GROUP BY platform
        ORDER BY views DESC
    """

    return pd.read_sql(query, engine, index_col="platform")


def fetch_content_type_summary(engine=None):
    """Get aggregated metrics by content type."""

    engine = engine or get_engine()

    query = """
        SELECT
            content_type,
            SUM(views)    AS views,
            SUM(likes)    AS likes,
            SUM(shares)   AS shares,
            SUM(comments) AS comments
        FROM media_events
        GROUP BY content_type
        ORDER BY views DESC
    """

    return pd.read_sql(query, engine, index_col="content_type")


# ~ Quick check
# --------------------------------------------------

if __name__ == "__main__":
    engine = get_engine()

    print("Testing DB connection...")
    create_schema(engine)

    print("\nPlatform summary:")
    try:
        print(fetch_platform_summary(engine))
    except ValueError as e:
        print(f"(No data yet) {e}")