#!/usr/bin/env python3
import os, psycopg2
from matplotlib import pyplot as plt
from dotenv import load_dotenv

def main():
    load_dotenv()

    PRODUCERS = os.getenv("PRODUCERS")
    PARTITIONS = os.getenv("PARTITIONS")
    CONSUMERS = os.getenv("CONSUMERS")

    PRODUCERS = 1 if PRODUCERS is None else int(PRODUCERS)
    PARTITIONS = 1 if PARTITIONS is None else int(PARTITIONS)
    CONSUMERS = 1 if CONSUMERS is None else int(CONSUMERS)

    PG_USER = os.getenv("PG_USER")
    PG_PASSWORD = os.getenv("PG_PASSWORD")
    PG_DATABASE = os.getenv("PG_DATABASE")
    PG_HOST = os.getenv("PG_HOST")
    PG_PORT = os.getenv("PG_PORT")

    report_file_name = f"PROD_{PRODUCERS}_PART_{PARTITIONS}_CONS_{CONSUMERS}"

    pg_conn = psycopg2.connect(user=PG_USER, password=PG_PASSWORD, database=PG_DATABASE, host=PG_HOST, port=PG_PORT)
    cur = pg_conn.cursor()

    cur.execute("""SELECT COUNT(*),
ROUND((MAX(processed) - MIN(created))/1000.0,2) AS total_time_sec,
ROUND(MAX(processed - created)/1000.0,2) AS max_latency_sec,
ROUND(SUM(size/1024.0/1024.0)*8/((MAX(processed) - MIN(processed))/1000.0),2) AS throughput_mbps
FROM kafka_throughput_metrics""")

    row = cur.fetchone()

    print(f"Total time: {row[1]} sec")
    print(f"Max latency: {row[2]} sec")
    print(f"Throughput: {row[3]} Mbps")

    with open(f"report_output/{report_file_name}.csv", 'w', newline='') as file:
        file.write(f"total_time,max_latency,throughput\n")
        file.write(f"{row[1]},{row[2]},{row[3]}\n")

    cur.execute("""WITH t AS (
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
ORDER BY bucket""")

    rows = cur.fetchall()
    
    time_sec = [r[1] for r in rows]
    max_latency_sec = [r[2] for r in rows]
    throughput_mbps = [r[3] for r in rows]

    cur.close()
    pg_conn.close()

    plt.subplot(2, 1, 1)
    plt.plot(time_sec, max_latency_sec)
    plt.ylabel('Max latency, sec')
    plt.title('Max latency and Throughput')

    plt.subplot(2, 1, 2)
    plt.plot(time_sec, throughput_mbps)
    plt.ylabel('Throughput, Mbps')
    plt.xlabel('Time, sec')
    
    plt.savefig(f"report_output/{report_file_name}.png")

if __name__ == '__main__':
    main()
