-- Stores social media content performance data
-- Used to track engagement metrics for KPI reporting
CREATE TABLE media_events (

    -- Unique ID for each content record
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    -- Platform where the content was posted
    platform TEXT,

    -- Type of content (Video, Reel, Post, Short, etc.)
    content_type TEXT,

    -- Number of views the content received
    views INTEGER,

    -- Number of likes received
    likes INTEGER,

    -- Number of times the content was shared
    shares INTEGER,

    -- Number of comments left by users
    comments INTEGER
);