#!/usr/bin/env python3
import csv, json
from kafka import KafkaProducer

def main():
    filepath = 'reddit_ds.csv'

    producer = KafkaProducer(bootstrap_servers=["localhost:9092"])

    with open(filepath, encoding="utf8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            print(row)
            json_data = json.dumps(row).encode('utf-8')
            print(json_data)
            #producer.poll(0)
            #row['producer_timestamp'] = int(time.time() * 1000)
            
            producer.send(topic="reddit_ds", value=json_data)
            #producer.flush()
            
if __name__ == '__main__':
    main()
