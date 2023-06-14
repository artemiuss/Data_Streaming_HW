#!/usr/bin/env python3
import os, time, json
from kafka import KafkaConsumer
from dotenv import load_dotenv

def main():
    load_dotenv()

    KAFKA_HOST = os.getenv("KAFKA_HOST")
    KAFKA_PORT = os.getenv("KAFKA_PORT")
    KAFKA_TOPIC = os.getenv("KAFKA_TOPIC")

    print(f"KAFKA_HOST: {KAFKA_HOST}")
    print(f"KAFKA_PORT: {KAFKA_PORT}")
    print(f"KAFKA_TOPIC: {KAFKA_TOPIC}")

    consumer = KafkaConsumer(
                                KAFKA_TOPIC,
                                bootstrap_servers=[f"{KAFKA_HOST}:{KAFKA_PORT}"],
                                auto_offset_reset='earliest',
                                value_deserializer=lambda m: json.loads(m.decode('utf-8'))
                            )
    for message in consumer:
        # message value and key are raw bytes -- decode if necessary!
        # e.g., for unicode: `message.value.decode('utf-8')`
        print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                            message.offset, message.key,
                                            message.value))
        time.sleep(1)

    consumer.close()

if __name__ == '__main__':
    main()

