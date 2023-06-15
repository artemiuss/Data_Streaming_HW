#!/usr/bin/env python3
import os
from kafka.admin import KafkaAdminClient
from kafka.errors import UnknownTopicOrPartitionError
from dotenv import load_dotenv

def main():
    load_dotenv()

    KAFKA_HOST = os.getenv("KAFKA_HOST")
    KAFKA_PORT = os.getenv("KAFKA_PORT")
    KAFKA_TOPIC = os.getenv("KAFKA_TOPIC")

    admin_client = KafkaAdminClient(bootstrap_servers=[f"{KAFKA_HOST}:{KAFKA_PORT}"])

    try:
        admin_client.delete_topics(topics=[KAFKA_TOPIC])
    except UnknownTopicOrPartitionError as e:
        pass

if __name__ == '__main__':
    main()

