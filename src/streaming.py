import os
from enum import Enum
from json import dumps, loads

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer


KAFKA_HOST = "kafka:9092"


class Consumer(AIOKafkaConsumer):
    """https://aiokafka.readthedocs.io/en/stable/consumer.html"""

    def __init__(self, *args, **kwargs):
        return super().__init__(
            *args,
            **kwargs,
            bootstrap_servers=KAFKA_HOST,
            security_protocol=os.environ.get("KAFKA_SECURITY_PROTOCOL", "PLAINTEXT"),
            sasl_mechanism=os.environ.get("KAFKA_SASL_MECHANISM", "PLAIN"),
            value_deserializer=loads,
        )

    @classmethod
    async def create(cls, *args, **kwargs):
        consumer = cls(*args, **kwargs)
        await consumer.start()
        return consumer


def message_serializer(msg) -> bytes:
    return dumps(msg).encode()


class Producer(AIOKafkaProducer):
    """https://aiokafka.readthedocs.io/en/stable/producer.html"""

    def __init__(self, *args, **kwargs):
        return super().__init__(
            *args,
            **kwargs,
            bootstrap_servers=KAFKA_HOST,
            security_protocol=os.environ.get("KAFKA_SECURITY_PROTOCOL", "PLAINTEXT"),
            sasl_mechanism=os.environ.get("KAFKA_SASL_MECHANISM", "PLAIN"),
            value_serializer=message_serializer,
        )

    @classmethod
    async def create(cls, *args, **kwargs):
        producer = cls(*args, **kwargs)
        await producer.start()
        return producer


class Topic(str, Enum):
    """
    Recommended topic naming structure:
    <data-center>.<domain>.<classification>.<description>.<version>
    https://devshawn.com/blog/apache-kafka-topic-naming-conventions/

    (Data center is being omitted to simplify demo).
    """
    CRAWL = "website.fct.crawl.0"
    CHANGE = "website.cdc.change.0"
    PAGERANK = "website.cdc.pagerank.0"
    NER = "website.cdc.ner.0"
    RELEVANCY = "website.cdc.relevancy.0"
