#!/usr/bin/env python3
import os, csv, json, time
from kafka import KafkaProducer

def main():
    
    DS_FILENAME = os.getenv("DS_FILENAME")
    KAFKA_HOST = os.getenv("KAFKA_HOST")
    KAFKA_PORT = os.getenv("KAFKA_PORT")
    KAFKA_TOPIC = os.getenv("KAFKA_TOPIC")

    producer = KafkaProducer(bootstrap_servers=[f"{KAFKA_HOST}:{KAFKA_PORT}"])

    with open(DS_FILENAME, encoding="utf8", newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            row['comment_ts'] = int(time.time())
            json_data = json.dumps(row).encode('utf-8')
            producer.send(topic=KAFKA_TOPIC, value=json_data)
        producer.flush()

    producer.close()

if __name__ == '__main__':
    main()
