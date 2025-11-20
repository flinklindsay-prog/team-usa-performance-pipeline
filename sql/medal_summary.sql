-- medal_summary.sql
-- SQL to aggregate medal counts by year and sport
-- sql/medal_summary.sql
-- Aggregate medals by year and sport for USA

SELECT
  year,
  sport,
  COUNT(DISTINCT name) AS total_athletes,
  SUM(CASE WHEN medal = 'Gold' THEN 1 ELSE 0 END) AS gold_count,
  SUM(CASE WHEN medal = 'Silver' THEN 1 ELSE 0 END) AS silver_count,
  SUM(CASE WHEN medal = 'Bronze' THEN 1 ELSE 0 END) AS bronze_count,
  SUM(CASE WHEN medal IN ('Gold','Silver','Bronze') THEN 1 ELSE 0 END) AS medal_count,
  AVG(age) AS avg_age
FROM clean_athletes
GROUP BY year, sport
ORDER BY year, sport;
