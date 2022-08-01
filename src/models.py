from pydantic import BaseModel


class WebSiteCrawl(BaseModel):
    domain: str


class WebSiteJobId(WebSiteCrawl):
    id: str


class WebSiteRelevancy(WebSiteJobId):
    relevancy: float
