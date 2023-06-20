#!/usr/bin/env python3
import sys, os, time, json, datetime, psycopg2, multiprocessing
from kafka import KafkaConsumer
from dotenv import load_dotenv

def consume(kafka_host, kafka_port, kafka_topic, pg_user, pg_password, pg_database, pg_host, pg_port):
    consumer = KafkaConsumer(
                                kafka_topic,
                                bootstrap_servers=[f"{kafka_host}:{kafka_port}"],
                                auto_offset_reset='earliest',
                                consumer_timeout_ms=10000,
                                value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                                enable_auto_commit=False,
                                group_id='my-group'
                            )
    pg_conn = psycopg2.connect(user=pg_user, password=pg_password, database=pg_database, host=pg_host, port=pg_port)
    cur = pg_conn.cursor()

    for message in consumer:
        print (f"partition={message.partition}, offset={message.offset}, key={message.key}, timestamp={message.timestamp}")
        #print (f"value={message.value}")
        time.sleep(0.01)
        created = int(message.value['created'])
        processed = int(datetime.datetime.utcnow().timestamp()*1e3)
        size = sys.getsizeof(json.dumps(message.value))
        cur.execute("INSERT INTO kafka_throughput_metrics (created, processed, size) VALUES (%s, %s, %s)"
                    ,(created, processed, size))
    
    pg_conn.commit()
    cur.close()
    consumer.close()

def main():
    load_dotenv()

    KAFKA_HOST = os.getenv("KAFKA_HOST")
    KAFKA_PORT = os.getenv("KAFKA_PORT")
    KAFKA_TOPIC = os.getenv("KAFKA_TOPIC")

    CONSUMERS = os.getenv("CONSUMERS")
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
    pg_conn.close()

    processes = []
    for i in range(CONSUMERS):
        p = multiprocessing.Process(target=consume, args=(KAFKA_HOST, KAFKA_PORT, KAFKA_TOPIC, PG_USER, PG_PASSWORD, PG_DATABASE, PG_HOST, PG_PORT,))
        processes.append(p)
        p.start()
    for p in processes:
        p.join()

if __name__ == '__main__':
    main()

