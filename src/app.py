from collections import defaultdict
from uuid import uuid4

from fastapi import FastAPI

from src.streaming import Consumer, Producer, Topic


CONSUMER = PRODUCER = None  # Initialize clients outside async context

EVENT_CACHE = defaultdict(dict)

APP = FastAPI()


@APP.on_event("startup")
async def start_streaming_clients():
    await Consumer.create(Topic.RELEVANCY.value)
    await Producer.create()
