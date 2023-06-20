WITH t AS (
SELECT t.*,
(MAX(processed) OVER(ORDER BY id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)- MIN(created) OVER(ORDER BY id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW))/1000.0 AS total_time_sec
FROM kafka_throughput_metrics t
)
,stats AS (
SELECT MIN(total_time_sec) AS time_min, MAX(total_time_sec) AS time_max
FROM t
)
SELECT
width_bucket(total_time_sec, time_min, time_max + 1, 20) AS bucket,
ROUND((MAX(processed) - MIN(created))/1000.0,-1) AS total_time_sec,
ROUND(MAX(processed - created)/1000.0,-1) AS max_latency_sec,
ROUND(SUM(size/1024.0/1024.0)*8/((MAX(processed) - MIN(processed))/1000.0),2) AS throughput_mbps
FROM t, stats
GROUP BY bucket
ORDER BY bucket
;

SELECT COUNT(*),
ROUND((MAX(processed) - MIN(created))/1000.0,2) AS total_time_sec,
ROUND(MAX(processed - created)/1000.0,2) AS max_latency_sec,
ROUND(SUM(size/1024.0/1024.0)*8/((MAX(processed) - MIN(processed))/1000.0),2) AS throughput_mbps
FROM kafka_throughput_metrics;


