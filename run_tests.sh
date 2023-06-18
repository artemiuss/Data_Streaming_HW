#!/bin/bash

# 1. One producer, a topic with one partition, one consumer
PRODUCERS=1
PARTITIONS=1
CONSUMERS=1

printf "PRODUCERS: ${PRODUCERS}\n"
printf "PARTITIONS: ${PARTITIONS}\n"
printf "CONSUMERS: ${CONSUMERS}\n"

docker compose up -d
while [ ! -f "PROD_${PRODUCERS}_PART_${PARTITIONS}_CONS_${CONSUMERS}" ]; do sleep 1; done

docker compose down

# 2. One producer, a topic with one partition, 2 consumers
PRODUCERS=1
PARTITIONS=1
CONSUMERS=2
printf "PRODUCERS: ${PRODUCERS}\n"
printf "PARTITIONS: ${PARTITIONS}\n"
printf "CONSUMERS: ${CONSUMERS}\n"

docker compose up -d
while [ ! -f "PROD_${PRODUCERS}_PART_${PARTITIONS}_CONS_${CONSUMERS}" ]; do sleep 1; done
docker compose down

# 3. One producer, a topic with 2 partitions, 2 consumers
PRODUCERS=1
PARTITIONS=2
CONSUMERS=2

printf "PRODUCERS: ${PRODUCERS}\n"
printf "PARTITIONS: ${PARTITIONS}\n"
printf "CONSUMERS: ${CONSUMERS}\n"

docker compose up -d
while [ ! -f "PROD_${PRODUCERS}_PART_${PARTITIONS}_CONS_${CONSUMERS}" ]; do sleep 1; done
docker compose down

# 4. One producer, a topic with 5 partitions, 5 consumers
PRODUCERS=1
PARTITIONS=5
CONSUMERS=5

printf "PRODUCERS: ${PRODUCERS}\n"
printf "PARTITIONS: ${PARTITIONS}\n"
printf "CONSUMERS: ${CONSUMERS}\n"

docker compose up -d
while [ ! -f "PROD_${PRODUCERS}_PART_${PARTITIONS}_CONS_${CONSUMERS}" ]; do sleep 1; done
docker compose down

# 5. One producer, a topic with 10 partitions, 1 consumers
PRODUCERS=1
PARTITIONS=10
CONSUMERS=1

printf "PRODUCERS: ${PRODUCERS}\n"
printf "PARTITIONS: ${PARTITIONS}\n"
printf "CONSUMERS: ${CONSUMERS}\n"

docker compose up -d
while [ ! -f "PROD_${PRODUCERS}_PART_${PARTITIONS}_CONS_${CONSUMERS}" ]; do sleep 1; done
docker compose down

# 6. One producer, a topic with 10 partitions, 5 consumers
PRODUCERS=1
PARTITIONS=10
CONSUMERS=5

printf "PRODUCERS: ${PRODUCERS}\n"
printf "PARTITIONS: ${PARTITIONS}\n"
printf "CONSUMERS: ${CONSUMERS}\n"

docker compose up -d
while [ ! -f "PROD_${PRODUCERS}_PART_${PARTITIONS}_CONS_${CONSUMERS}" ]; do sleep 1; done
docker compose down

# 7. One producer, a topic with 10 partitions, 10 consumers
PRODUCERS=1
PARTITIONS=10
CONSUMERS=10

printf "PRODUCERS: ${PRODUCERS}\n"
printf "PARTITIONS: ${PARTITIONS}\n"
printf "CONSUMERS: ${CONSUMERS}\n"

docker compose up -d
while [ ! -f "PROD_${PRODUCERS}_PART_${PARTITIONS}_CONS_${CONSUMERS}" ]; do sleep 1; done
docker compose down

# 8. 2 producers (input data should be split into 2 parts somehow), a topic with 10 partitions, 10 consumers
PRODUCERS=2
PARTITIONS=10
CONSUMERS=10

printf "PRODUCERS: ${PRODUCERS}\n"
printf "PARTITIONS: ${PARTITIONS}\n"
printf "CONSUMERS: ${CONSUMERS}\n"

docker compose up -d
while [ ! -f "PROD_${PRODUCERS}_PART_${PARTITIONS}_CONS_${CONSUMERS}" ]; do sleep 1; done
docker compose down

# Build final report
final_report.py
