#!/usr/bin/env python3
import time, json
from kafka import KafkaConsumer

def main():
    consumer = KafkaConsumer(
                                'reddit_ds',
                                bootstrap_servers=["localhost:9092"],
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

