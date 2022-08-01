from collections import defaultdict
from uuid import uuid4

from fastapi import FastAPI

from src.streaming import Consumer, Producer, Topic


CONSUMER = Consumer(Topic.RELEVANCY)

PRODUCER = Producer()

EVENT_CACHE = defaultdict(dict)

APP = FastAPI()


@APP.on_event("startup")
async def start_streaming_clients():
    await CONSUMER.start()
    await PRODUCER.start()
