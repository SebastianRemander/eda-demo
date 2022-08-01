# Kafka demo

> Apache Kafka is a distributed streaming platform used for building real-time applications


NOTE: **This project is only intended for local development**. For production use (with the bitnami images), please refer [here](https://hub.docker.com/r/bitnami/kafka/) for secure configuration and deployment suggestions.


## Get started
1. Install `docker`, `docker-compose`.

2. Build the local image that'll run the producer/consumer apps:

`docker build -t pykafka/base .`

3. Spin up the whole stack of apps, kafka, and zookeeper:

`docker-compose up --force-recreate --always-recreate-deps --renew-anon-volumes`

4. Navigate to localhost:5000/docs with your favorite browser to check out a simple website crawling system

5. Stop

`docker-compose down --volumes`


## Troubleshooting

If kafka errors on start-up, `docker volume prune` may help.
