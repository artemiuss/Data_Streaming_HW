WITH stats AS (
SELECT MIN(processed) AS time_min_processed, MAX(processed) AS time_max_processed,
MIN(created) AS time_min_created, MAX(created) AS time_max_created
FROM kafka_throughput_metrics
)
SELECT
width_bucket(processed, time_min_processed, time_max_processed + 1, 100) AS bucket,
ROUND((MAX(processed) - MAX(time_min_created))/1000.0,2) AS total_time_sec,
ROUND(MAX(processed - created)/1000.0,2) AS max_latency_sec,
ROUND(SUM(size/1024.0/1024.0)*8/((MAX(processed) - MIN(processed))/1000.0),2) AS throughput_mbps
FROM kafka_throughput_metrics, stats
GROUP BY bucket
ORDER BY bucket
;

SELECT COUNT(*),
ROUND((MAX(processed) - MIN(created))/1000.0,2) AS total_time_sec,
ROUND(MAX(processed - created)/1000.0,2) AS max_latency_sec,
ROUND(SUM(size/1024.0/1024.0)*8/((MAX(processed) - MIN(processed))/1000.0),2) AS throughput_mbps
FROM kafka_throughput_metrics
;

