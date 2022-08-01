import asyncio
from json import dumps
from random import randint

from src.streaming import Consumer, Producer, Topic


GROUP_ID = "WEBSITE_CHANGES"


async def amain():
    """Consume website crawl result, produce parsed changes."""
    consumer = await Consumer.create(Topic.CRAWL.value, group_id=GROUP_ID)
    producer = await Producer.create()
    async for message in consumer:
        data = message.value
        await producer.send_and_wait(Topic.CHANGE.value, parse_website_change(data))


def parse_website_change(data: dict) -> bytes:
    return dumps(
        {
            "domain": data["domain"],
            "id": data["id"],
            "content": data["content"],
            "content_old": "<div>Hello World</div>",
            # some business critical parsing
            "content_diff": {"-": "World", "+": "Kafka",},
            "n_of_links": randint(0, 10),
            "n_of_links_diff": randint(-5, 5),
        }
    ).encode()


if __name__ == "__main__":
    asyncio.run(amain())
