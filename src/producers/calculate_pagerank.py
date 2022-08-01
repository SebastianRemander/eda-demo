import asyncio
from json import dumps
from random import randint

from src.streaming import Consumer, Producer, Topic


GROUP_ID = "WEBSITE_PAGERANK"


async def amain():
    """Consume website changes, produce pagerank results."""
    consumer = await Consumer.create(Topic.CHANGE.value, group_id=GROUP_ID)
    producer = await Producer.create()
    async for message in consumer:
        data = message.value
        await producer.send_and_wait(Topic.PAGERANK.value, await calculate_pagerank(data))


async def calculate_pagerank(data: dict) -> bytes:
    await asyncio.sleep(2)  # a db visit to check other websites linking to this
    links_in = randint(0, 10)
    links_out = data["n_of_links"]
    return dumps(
        {
            "domain": data["domain"],
            "id": data["id"],
            "pagerank": links_in + links_out + data["n_of_links_diff"],
        }
    ).encode()


if __name__ == "__main__":
    asyncio.run(amain())
