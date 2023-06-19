#!/usr/bin/env python3
import os, csv, json, datetime, multiprocessing
from kafka import KafkaProducer
from dotenv import load_dotenv

def produce(filename, kafka_host, kafka_port, kafka_topic):
    producer = KafkaProducer(bootstrap_servers=[f"{kafka_host}:{kafka_port}"])

    with open(filename, encoding="utf8", newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            row['created'] = int(datetime.datetime.utcnow().timestamp()*1e3)
            #row['created'] = int(float(row['created']))
            json_data = json.dumps(row).encode('utf-8')
            print(json_data)
            producer.send(topic=kafka_topic, value=json_data)
        producer.flush()

    producer.close()

def main():
    load_dotenv()
    
    DS_FILENAME = os.getenv("DS_FILENAME")
    KAFKA_HOST = os.getenv("KAFKA_HOST")
    KAFKA_PORT = os.getenv("KAFKA_PORT")
    KAFKA_TOPIC = os.getenv("KAFKA_TOPIC")

    PRODUCERS = os.getenv("PRODUCERS")
    PRODUCERS = 1 if PRODUCERS is None else int(PRODUCERS)

    if PRODUCERS == 1:
        produce(DS_FILENAME, KAFKA_HOST, KAFKA_PORT, KAFKA_TOPIC)
    elif PRODUCERS > 1:
        filename = os.path.splitext(DS_FILENAME)[0]
        extension = os.path.splitext(DS_FILENAME)[1]

        processes = []
        for i in range(PRODUCERS):
            p = multiprocessing.Process(target=produce, args=(f"{filename}_part_{i}{extension}", KAFKA_HOST, KAFKA_PORT, KAFKA_TOPIC,))
            processes.append(p)
            p.start()
        for p in processes:
            p.join()

if __name__ == '__main__':
    main()
