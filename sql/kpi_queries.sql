-- KPI: Total content published
SELECT COUNT(*) AS total_content
FROM media_events;

-- KPI: Total views across all content
SELECT SUM(views) AS total_views
FROM media_events;

-- KPI: Overall engagement rate
SELECT
    SUM(likes + shares + comments) * 1.0 /
    SUM(views) AS engagement_rate
FROM media_events;

-- KPI: Highest-performing platform by views
SELECT
    platform,
    SUM(views) AS total_views
FROM media_events
GROUP BY platform
ORDER BY total_views DESC
LIMIT 1;