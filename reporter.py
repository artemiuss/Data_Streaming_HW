#!/usr/bin/env python3
import os, psycopg2
from datetime import datetime
from matplotlib import pyplot as plt
from dotenv import load_dotenv

def plot_latency(latency):
    plt.plot(latency)
    plt.ylabel('Latency in seconds')
    plt.xlabel('Time in seconds')
    plt.show()

def plot_throughput(throughput):
    plt.plot(throughput)
    plt.ylabel('Mbps')
    plt.xlabel('Time in seconds')
    plt.show()

def plot(mbps, latencies):
    plot_latency(latencies)
    plot_throughput(mbps)

def main():
    load_dotenv()
    
    PG_USER = os.getenv("PG_USER")
    PG_PASSWORD = os.getenv("PG_PASSWORD")
    PG_DATABASE = os.getenv("PG_DATABASE")
    PG_HOST = os.getenv("PG_HOST")
    PG_PORT = os.getenv("PG_PORT")

    pg_conn = psycopg2.connect(user=PG_USER, password=PG_PASSWORD, database=PG_DATABASE, host=PG_HOST, port=PG_PORT)
    cur = pg_conn.cursor()

    cur.execute("""SELECT (MAX(processed) - MIN(created))/1000.0 AS total_time_sec,
                   MAX(processed - created)/1000.0 AS max_latency_sec,
                   ROUND(SUM(size/1024.0/1024.0)*8/((MAX(processed) - MIN(created))/1000.0),2) AS throughput_mbps
                   FROM kafka_throughput_metrics
                """)

    row = cur.fetchone()
    cur.close()
    pg_conn.close()

    print(f"Total time: {row[0]} sec")
    print(f"Max latency: {row[1]} sec")
    print(f"Throughput: {row[2]} Mbps")

    #with open('report.txt', 'a', newline='') as file:
    #    file.write(f"{datetime.now().strftime('%Y.%m.%d %H:%M:%S')} Total time: {row[0]} sec, Max latency: {row[0]} sec, Throughput: {row[1]} Mbps\n")

if __name__ == '__main__':
    main()
