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

    cur.execute("""WITH stats AS (
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
""")

    rows = cur.fetchall()
    
    time_sec = [r[1] for r in rows]
    max_latency_sec = [r[2] for r in rows]
    throughput_mbps = [r[3] for r in rows]

    cur.close()
    pg_conn.close()

    plt.subplot(2, 1, 1)
    plt.plot(time_sec, max_latency_sec)
    plt.ylabel('Max Latency, sec')
    plt.title('Max Latency and Throughput')

    plt.subplot(2, 1, 2)
    plt.plot(time_sec, throughput_mbps)
    plt.ylabel('Throughput, Mbps')
    plt.xlabel('Time, sec')
    
    plt.savefig(f"report_output/{report_file_name}.png")

if __name__ == '__main__':
    main()
