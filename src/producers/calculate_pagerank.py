import asyncio
import logging
from json import dumps
from random import randint

from src.streaming import Consumer, Producer, Topic


LOGGER = logging.getLogger(__name__)


GROUP_ID = "WEBSITE_PAGERANK"


async def amain():
    """Consume website changes, produce pagerank results."""
    consumer = await Consumer.create(Topic.CHANGE.value, group_id=GROUP_ID)
    producer = await Producer.create()
    async for message in consumer:
        data = message.value
        LOGGER.info("processing event %s %s", data["id"], data["domain"])
        await producer.send_and_wait(Topic.PAGERANK.value, await calculate_pagerank(data))


async def calculate_pagerank(data: dict) -> dict:
    await asyncio.sleep(2)  # a db visit to check other websites linking to this
    links_in = randint(0, 10)
    links_out = data["n_of_links"]
    return {
        "domain": data["domain"],
        "id": data["id"],
        "pagerank": links_in + links_out + data["n_of_links_diff"],
    }


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s [%(module)s:%(lineno)s] %(message)s')
    asyncio.run(amain())
