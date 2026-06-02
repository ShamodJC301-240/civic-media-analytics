-- Where the KPI queries will end up

-- Total content pieces
SELECT COUNT(*) AS total_content
FROM media_events;

-- Total engagement per platform
SELECT platform,
       SUM(views) AS total_views,
       SUM(likes) AS total_likes,
       SUM(shares) AS total_shares,
       SUM(comments) AS total_comments
FROM media_events
GROUP BY platform
ORDER BY total_views DESC;

-- Engagement rates
SELECT platform,
       SUM(likes + shares + comments)::float / NULLIF(SUM(views), 0) AS engagement_rate
FROM media_events
GROUP BY platform;

-- Top performing content types
SELECT content_type,
       SUM(views) AS total_views
FROM media_events
GROUP BY content_type
ORDER BY total_views DESC;