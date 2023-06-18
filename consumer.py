#!/usr/bin/env python3
import sys, os, time, json, datetime, psycopg2
from kafka import KafkaConsumer
from dotenv import load_dotenv
import subprocess

def main():
    load_dotenv()

    KAFKA_HOST = os.getenv("KAFKA_HOST")
    KAFKA_PORT = os.getenv("KAFKA_PORT")
    KAFKA_TOPIC = os.getenv("KAFKA_TOPIC")

    PRODUCERS = os.getenv("PRODUCERS")
    PARTITIONS = os.getenv("PARTITIONS")
    CONSUMERS = os.getenv("CONSUMERS")

    PRODUCERS = 1 if PRODUCERS is None else int(PRODUCERS)
    PARTITIONS = 1 if PARTITIONS is None else int(PARTITIONS)
    CONSUMERS = 1 if CONSUMERS is None else int(CONSUMERS)

    PG_USER = os.getenv("PG_USER")
    PG_PASSWORD = os.getenv("PG_PASSWORD")
    PG_DATABASE = os.getenv("PG_DATABASE")
    PG_HOST = os.getenv("PG_HOST")
    PG_PORT = os.getenv("PG_PORT")

    # wait PostreSQL to start
    while True:
        try:
            pg_conn = psycopg2.connect(user=PG_USER, password=PG_PASSWORD, database=PG_DATABASE, host=PG_HOST, port=PG_PORT)
            pg_conn.close()
            print("PostgreSQL has started successfully.")
            break
        except psycopg2.OperationalError as e:
            time.sleep(1)
    
    pg_conn = psycopg2.connect(user=PG_USER, password=PG_PASSWORD, database=PG_DATABASE, host=PG_HOST, port=PG_PORT)
    cur = pg_conn.cursor()
    
    cur.execute("DROP TABLE IF EXISTS kafka_throughput_metrics")
    cur.execute("""CREATE TABLE kafka_throughput_metrics (
                    id SERIAL,
                    created BIGINT NOT NULL,
                    processed BIGINT NOT NULL,
                    size BIGINT NOT NULL,
                    PRIMARY KEY (id))""")
    pg_conn.commit()

    consumer = KafkaConsumer(
                                KAFKA_TOPIC,
                                bootstrap_servers=[f"{KAFKA_HOST}:{KAFKA_PORT}"],
                                auto_offset_reset='earliest', # consume earliest available messages, don't commit offsets
                                consumer_timeout_ms=1000, # StopIteration if no message after 1sec
                                value_deserializer=lambda m: json.loads(m.decode('utf-8'))
                            )
    for message in consumer:
        print (f"partition={message.partition}, offset={message.offset}, key={message.key}, timestamp={message.timestamp}")
        #print (f"value={message.value}")
        #time.sleep(1)
        created = int(message.value['created'])
        processed = int(datetime.datetime.utcnow().timestamp()*1e3)
        size = sys.getsizeof(json.dumps(message.value))
        cur.execute("INSERT INTO kafka_throughput_metrics (created, processed, size) VALUES (%s, %s, %s)"
                    ,(created, processed, size))
        pg_conn.commit()

    consumer.close()
    cur.close()
    pg_conn.close()

if __name__ == '__main__':
    main()

