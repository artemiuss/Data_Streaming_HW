# Data Streaming Homework

...

## Preparation
```
git clone https://github.com/conduktor/kafka-stack-docker-compose.git
```

## Set up
```
cd kafka-stack-docker-compose
docker compose -f zk-single-kafka-multiple.yml up -d
```

## Usage notes

...


## Clean-Up
```
docker compose -f zk-single-kafka-multiple.yml down --rmi all -v --remove-orphans
```
