#!/usr/bin/env python3
import psycopg2

def main():
    pg_conn = psycopg2.connect(user="kafka_test", password="kafka_test", database="kafka_test", host="postgres", port=5432)
    cur = pg_conn.cursor()

    result = cur.fetchval("""SELECT ROUND(MAX(latency),2) AS max_latency_sec,
                             ROUND((MAX(message_created) - MIN(message_created))/(SUM(size)/1024/1024),2) AS throughput_mbps
                             FROM kafka_throughput_metrics""")

    print(f"Max latency: {result[0]} sec")
    print(f"Throughput: {result[1]} Mbps")
    
    cur.close()
    pg_conn.close()

if __name__ == '__main__':
    main()
