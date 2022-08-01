import asyncio
import logging
from collections import defaultdict
from json import dumps
from random import randint

from src.streaming import Consumer, Producer, Topic


LOGGER = logging.getLogger(__name__)


GROUP_ID = "WEBSITE_RELEVANCY"


async def amain():
    """Consume pagerank and ner results, produce website relevancy results."""
    consumer = await Consumer.create(Topic.NER.value, Topic.PAGERANK.value, group_id=GROUP_ID)
    producer = await Producer.create()
    cache = defaultdict(dict)  # for storing the consumed results for the same change event
    async for message in consumer:
        data = message.value
        cached_event = cache[data["id"]]
        cached_event["domain"] = data["domain"]
        cached_event["id"] = data["id"]
        if message.topic == Topic.NER:
            cached_event["ner"] = data["ner"]
        if message.topic == Topic.PAGERANK:
            cached_event["pagerank"] = data["pagerank"]
        if "ner" in cached_event and "pagerank" in cached_event:
            LOGGER.info("processing event %s %s", cached_event["id"], cached_event["domain"])
            await producer.send_and_wait(Topic.RELEVANCY.value, calculate_relevancy(cached_event))
            del cache[data["id"]]  # release storage


def calculate_relevancy(data: dict) -> bytes:
    relevancy = data["pagerank"] + data["ner"]["persons"] + data["ner"]["brands"] / 2
    return dumps(
        {
            "domain": data["domain"],
            "id": data["id"],
            "relevancy": relevancy,
        }
    ).encode()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s [%(module)s:%(lineno)s] %(message)s')
    asyncio.run(amain())
