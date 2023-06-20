#!/usr/bin/env python3
import csv
from matplotlib import pyplot as plt

test_names = [
    'PRODUCERS=1\nPARTITIONS=1\nCONSUMERS=1',# 1. One producer, a topic with one partition, one consumer
    'PRODUCERS=1\nPARTITIONS=1\nCONSUMERS=2', # 2. One producer, a topic with one partition, 2 consumers
    'PRODUCERS=1\nPARTITIONS=2\nCONSUMERS=2', # 3. One producer, a topic with 2 partitions, 2 consumers
    'PRODUCERS=1\nPARTITIONS=5\nCONSUMERS=5', # 4. One producer, a topic with 5 partitions, 5 consumers
    'PRODUCERS=1\nPARTITIONS=10\nCONSUMERS=1', # 5. One producer, a topic with 10 partitions, 1 consumers
    'PRODUCERS=1\nPARTITIONS=10\nCONSUMERS=5', # 6. One producer, a topic with 10 partitions, 5 consumers
    'PRODUCERS=1\nPARTITIONS=10\nCONSUMERS=10', # 7. One producer, a topic with 10 partitions, 10 consumers
    'PRODUCERS=2\nPARTITIONS=10\nCONSUMERS=10' # 8. 2 producers (input data should be split into 2 parts somehow), a topic with 10 partitions, 10 consumers
]

time_sec = []
max_latency_sec = []
throughput_mbps = []

def collect_metrics(file_name):
    with open(file_name, encoding="utf8", newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            time_sec.append(float(row['total_time']))
            max_latency_sec.append(float(row['max_latency']))
            throughput_mbps.append(float(row['throughput']))

def main():
    # 1. One producer, a topic with one partition, one consumer
    PRODUCERS=1
    PARTITIONS=1
    CONSUMERS=1

    collect_metrics(f"report_output/PROD_{PRODUCERS}_PART_{PARTITIONS}_CONS_{CONSUMERS}.csv")

    # 2. One producer, a topic with one partition, 2 consumers
    PRODUCERS=1
    PARTITIONS=1
    CONSUMERS=2

    collect_metrics(f"report_output/PROD_{PRODUCERS}_PART_{PARTITIONS}_CONS_{CONSUMERS}.csv")

    # 3. One producer, a topic with 2 partitions, 2 consumers
    PRODUCERS=1
    PARTITIONS=2
    CONSUMERS=2

    collect_metrics(f"report_output/PROD_{PRODUCERS}_PART_{PARTITIONS}_CONS_{CONSUMERS}.csv")

    # 4. One producer, a topic with 5 partitions, 5 consumers
    PRODUCERS=1
    PARTITIONS=5
    CONSUMERS=5

    collect_metrics(f"report_output/PROD_{PRODUCERS}_PART_{PARTITIONS}_CONS_{CONSUMERS}.csv")

    # 5. One producer, a topic with 10 partitions, 1 consumers
    PRODUCERS=1
    PARTITIONS=10
    CONSUMERS=1

    collect_metrics(f"report_output/PROD_{PRODUCERS}_PART_{PARTITIONS}_CONS_{CONSUMERS}.csv")

    # 6. One producer, a topic with 10 partitions, 5 consumers
    PRODUCERS=1
    PARTITIONS=10
    CONSUMERS=5

    collect_metrics(f"report_output/PROD_{PRODUCERS}_PART_{PARTITIONS}_CONS_{CONSUMERS}.csv")

    # 7. One producer, a topic with 10 partitions, 10 consumers
    PRODUCERS=1
    PARTITIONS=10
    CONSUMERS=10

    collect_metrics(f"report_output/PROD_{PRODUCERS}_PART_{PARTITIONS}_CONS_{CONSUMERS}.csv")

    # 8. 2 producers (input data should be split into 2 parts somehow), a topic with 10 partitions, 10 consumers
    PRODUCERS=2
    PARTITIONS=10
    CONSUMERS=10

    collect_metrics(f"report_output/PROD_{PRODUCERS}_PART_{PARTITIONS}_CONS_{CONSUMERS}.csv")

    plt.title('Total Time')
    plt.bar(test_names, time_sec)
    plt.ylabel('Total time, sec')
    plt.xticks(fontsize=8, rotation=90)
    plt.savefig(f"report_output/final_report_total_time.png", bbox_inches='tight', pad_inches=0.1, dpi=300)
    plt.cla()

    plt.title('Max Latency')
    plt.bar(test_names, max_latency_sec)
    plt.ylabel('Max Latency, sec')
    plt.xticks(fontsize=9, rotation=90)
    plt.savefig(f"report_output/final_report_latency.png", bbox_inches='tight', pad_inches=0.1, dpi=300)
    plt.cla()

    plt.title('Throughput')
    plt.bar(test_names, throughput_mbps)
    plt.ylabel('Throughput, Mbps')
    plt.xticks(fontsize=8, rotation=90)
    plt.savefig(f"report_output/final_report_throughput.png", bbox_inches='tight', pad_inches=0.1, dpi=300)
    plt.cla()

if __name__ == '__main__':
    main()

