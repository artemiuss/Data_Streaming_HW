#!/usr/bin/env python3
import sys, os, time, json, datetime, psycopg2
from kafka import KafkaConsumer
from dotenv import load_dotenv

def main():
    load_dotenv()

    KAFKA_HOST = os.getenv("KAFKA_HOST")
    KAFKA_PORT = os.getenv("KAFKA_PORT")
    KAFKA_TOPIC = os.getenv("KAFKA_TOPIC")

    pg_conn = psycopg2.connect(user="kafka_test", password="kafka_test", database="kafka_test", host="postgres", port=5433)
    cur = pg_conn.cursor()
    
    query = """DROP TABLE IF EXISTS kafka_throughput_metrics"""
    cur.execute(query)
    
    query = """CREATE TABLE kafka_throughput_metrics (
                id SERIAL,
                message_created INT UNSIGNED NOT NULL,
                latency INT UNSIGNED NOT NULL,
                size INT UNSIGNED NOT NULL,
                PRIMARY KEY (id))"""
    cur.execute(query)
    
    query = "INSERT INTO kafka_throughput_metrics (message_created, latency, size) VALUES ($1, $2, $3)"
    
    consumer = KafkaConsumer(
                                KAFKA_TOPIC,
                                bootstrap_servers=[f"{KAFKA_HOST}:{KAFKA_PORT}"],
                                auto_offset_reset='earliest',
                                value_deserializer=lambda m: json.loads(m.decode('utf-8'))
                            )
    for message in consumer:
        print (f"partition={message.partition}, offset={message.offset}, key={message.key}, timestamp={message.timestamp}")
        print (f"value={message.value}")
        time.sleep(1)
        message_created = message.value['created']
        processed = int(datetime.datetime.utcnow().timestamp()*1e3)
        latency = processed - message.timestamp
        size = sys.getsizeof(message.value)
        cur.execute(query, message_created, latency, size)
        pg_conn.commit()

    consumer.close()
    cur.close()
    pg_conn.close()

if __name__ == '__main__':
    main()

