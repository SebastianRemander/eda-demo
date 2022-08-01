import asyncio
import logging
from random import randint

from src.streaming import Consumer, Producer, Topic


LOGGER = logging.getLogger(__name__)


GROUP_ID = "WEBSITE_NER"


async def amain():
    """Consume website changes, produce NER results."""
    consumer = await Consumer.create(Topic.CHANGE.value, group_id=GROUP_ID)
    producer = await Producer.create()
    async for message in consumer:
        data = message.value
        LOGGER.info("processing event %s %s", data["id"], data["domain"])
        await producer.send_and_wait(Topic.NER.value, calculate_ner(data))


def calculate_ner(data: dict) -> dict:
    return {
        "domain": data["domain"],
        "id": data["id"],
        # some fancy NER detection results
        "ner": {
            "persons": randint(0, 10),
            "locations": randint(0, 10),
            "brands": randint(0, 10),
        },
    }


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s [%(module)s:%(lineno)s] %(message)s')
    asyncio.run(amain())
