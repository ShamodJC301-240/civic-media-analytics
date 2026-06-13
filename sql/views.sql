-- Aggregate engagement metrics by platform
CREATE VIEW platform_summary AS
SELECT
    platform,
    SUM(views) AS total_views,
    SUM(likes) AS total_likes,
    SUM(shares) AS total_shares,
    SUM(comments) AS total_comments
FROM media_events
GROUP BY platform;

-- Aggregate engagement metrics by content type
CREATE VIEW content_type_summary AS
SELECT
    content_type,
    SUM(views) AS total_views,
    SUM(likes) AS total_likes,
    SUM(shares) AS total_shares,
    SUM(comments) AS total_comments
FROM media_events
GROUP BY content_type;


