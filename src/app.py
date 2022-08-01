from functools import lru_cache
from json import dumps
from typing import Any, Mapping
from uuid import uuid4

from fastapi import FastAPI

from src.models import (
    WebSiteCrawl,
    WebSiteJobId,
    WebSiteRelevancy,
)
from src.streaming import Consumer, Producer, Topic


CONSUMER = PRODUCER = None  # Initialize clients outside async context

APP = FastAPI()


@APP.post("/crawl", response_model=WebSiteJobId, status_code=201)
async def simulate_website_crawl_result(
    request: WebSiteCrawl,
) -> WebSiteJobId:
    """
    Produce the requested domain as a crawl result, to simulate a website change event.
    """
    job_id = str(uuid4())
    payload = {"domain": request.domain, "id": job_id, "content": "<div>Hello Kafka</div>"}
    await PRODUCER.send_and_wait(Topic.CRAWL.value, dumps(payload).encode())
    return payload


@APP.get("/website_relevancy/{job_id}", response_model=WebSiteRelevancy)
async def get_website_relevancy(
    job_id: str,
) -> WebSiteRelevancy:
    """
    Get website relevancy for a given id, i.e., get relevancy value at a certain
    point in time.
    """
    return await CACHE.get_website_relevancy_event(job_id)


class Cache:

    def __init__(self):
        self.cache = {}

    async def get_website_relevancy_event(self, job_id: str) -> Mapping[str, Any]:
        if cached_event := self.cache.get(job_id):
            return cached_event
        async for message in CONSUMER:
            event = message.value
            if event.get("id") == job_id:
                self.cache[job_id] = event
                return event


CACHE = Cache()


@APP.on_event("startup")
async def start_streaming_clients():
    global CONSUMER
    global PRODUCER
    CONSUMER = await Consumer.create(Topic.RELEVANCY.value)
    PRODUCER = await Producer.create()


@APP.on_event("shutdown")
async def stop_streaming_clients():
    global CONSUMER
    global PRODUCER
    await CONSUMER.stop()
    await PRODUCER.stop()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.app:APP",
        host="0.0.0.0",
        port=5000,
        reload=True,
    )
