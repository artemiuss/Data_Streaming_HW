#!/usr/bin/env python3
import csv
from matplotlib import pyplot as plt

test_names = [1,2,3,4,5,6,7,8]
time_sec = []
max_latency_sec = []
throughput_mbps = []

def collect_metrics(file_name):
    with open(file_name, encoding="utf8", newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            time_sec.append(row['total time'])
            time_sec.append(row['max latency'])
            time_sec.append(row['throughput'])

def main():
    # 1. One producer, a topic with one partition, one consumer
    PRODUCERS=1
    PARTITIONS=1
    CONSUMERS=1

    collect_metrics(f"PROD_{PRODUCERS}_PART_{PARTITIONS}_CONS_{CONSUMERS}")

    # 2. One producer, a topic with one partition, 2 consumers
    PRODUCERS=1
    PARTITIONS=1
    CONSUMERS=2

    collect_metrics(f"PROD_{PRODUCERS}_PART_{PARTITIONS}_CONS_{CONSUMERS}")

    # 3. One producer, a topic with 2 partitions, 2 consumers
    PRODUCERS=1
    PARTITIONS=2
    CONSUMERS=2

    collect_metrics(f"PROD_{PRODUCERS}_PART_{PARTITIONS}_CONS_{CONSUMERS}")

    # 4. One producer, a topic with 5 partitions, 5 consumers
    PRODUCERS=1
    PARTITIONS=5
    CONSUMERS=5

    collect_metrics(f"PROD_{PRODUCERS}_PART_{PARTITIONS}_CONS_{CONSUMERS}")

    # 5. One producer, a topic with 10 partitions, 1 consumers
    PRODUCERS=1
    PARTITIONS=10
    CONSUMERS=1

    collect_metrics(f"PROD_{PRODUCERS}_PART_{PARTITIONS}_CONS_{CONSUMERS}")

    # 6. One producer, a topic with 10 partitions, 5 consumers
    PRODUCERS=1
    PARTITIONS=10
    CONSUMERS=5

    collect_metrics(f"PROD_{PRODUCERS}_PART_{PARTITIONS}_CONS_{CONSUMERS}")

    # 7. One producer, a topic with 10 partitions, 10 consumers
    PRODUCERS=1
    PARTITIONS=10
    CONSUMERS=10

    collect_metrics(f"PROD_{PRODUCERS}_PART_{PARTITIONS}_CONS_{CONSUMERS}")

    # 8. 2 producers (input data should be split into 2 parts somehow), a topic with 10 partitions, 10 consumers
    PRODUCERS=2
    PARTITIONS=10
    CONSUMERS=10

    collect_metrics(f"PROD_{PRODUCERS}_PART_{PARTITIONS}_CONS_{CONSUMERS}")

    plt.subplot(2, 1, 1)
    plt.plot(test_names, time_sec)
    plt.ylabel('Total time, sec')
    plt.title('Kafka Metrics')

    plt.subplot(2, 1, 2)
    plt.plot(test_names, max_latency_sec)
    plt.ylabel('Max latency, sec')

    plt.subplot(2, 1, 3)
    plt.plot(test_names, throughput_mbps)
    plt.ylabel('Throughput, Mbps')
    plt.xlabel('Test #')
    
    plt.savefig(f"report_output/final_report.png")
    
if __name__ == '__main__':
    main()

