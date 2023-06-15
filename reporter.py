#!/usr/bin/env python3
import psycopg2
from datetime import datetime

def main():
    pg_conn = psycopg2.connect(user="kafka_test", password="kafka_test", database="kafka_test", host="localhost", port=5433)
    cur = pg_conn.cursor()

    cur.execute("""SELECT ROUND((MAX(message_created) - MIN(message_created))/1000) AS total_time_sec,
                   ROUND(MAX(latency),2) AS max_latency_sec,
                   ROUND(((MAX(message_created) - MIN(message_created))/1000)/(SUM(size)/1024/1024),2) AS throughput_mbps
                   FROM kafka_throughput_metrics""")

    row = cur.fetchone()
    cur.close()
    pg_conn.close()

    print(f"Total time: {row[0]} sec")
    print(f"Max latency: {row[1]} sec")
    print(f"Throughput: {row[2]} Mbps")

    with open('report.txt', 'a', newline='') as file:
        file.write(f"{datetime.now().strftime('%Y.%m.%d %H:%M:%S')} Total time: {row[0]} sec, Max latency: {row[0]} sec, Throughput: {row[1]} Mbps\n")

if __name__ == '__main__':
    main()
