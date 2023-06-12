#!/usr/bin/env python3
import csv, json, time
from kafka import KafkaProducer

def main():
    filepath = 'reddit_ds.csv'

    producer = KafkaProducer(bootstrap_servers=["localhost:9092"])


    with open(filepath, encoding="utf8", newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            row['comment_ts'] = int(time.time())
            json_data = json.dumps(row).encode('utf-8')
            producer.send(topic="reddit_ds", value=json_data)
        producer.flush()
    producer.close()

if __name__ == '__main__':
    main()
