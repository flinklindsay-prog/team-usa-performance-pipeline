-- clean_athletes.sql
-- SQL for cleaning raw athlete data
-- sql/clean_athletes.sql
-- Assumes raw staging table raw_athletes exists with original column names
-- Purpose: create a clean athletes table for USA

CREATE TABLE IF NOT EXISTS clean_athletes AS
SELECT
  id,
  name,
  sex,
  CASE WHEN TRY_CAST(age AS INTEGER) IS NULL THEN NULL ELSE CAST(age AS INTEGER) END AS age,
  height,
  weight,
  team,
  noc,
  games,
  CAST(year AS INTEGER) AS year,
  season,
  city,
  sport,
  event,
  CASE
    WHEN medal = '' THEN 'None'
    WHEN medal IS NULL THEN 'None'
    ELSE INITCAP(medal)
  END AS medal
FROM raw_athletes
WHERE noc = 'USA';
