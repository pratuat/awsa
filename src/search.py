import logging
import asyncio
import googlesearch
import yahoo_search
from itertools import chain
from abc import ABC, abstractmethod

logger = logging.getLogger()


class Search(ABC):
    def __init__(self, id):
        self.id = id

    async def search(self, query):
        logger.info(f"{self.id} is searching query: {query}")
        result = await asyncio.to_thread(self._search, query)
        logger.info(f"{self.id} has returned query: {query}")
        return result

    @abstractmethod
    def _search(self, query):
        pass


class GoogleSearch(Search):
    def __init__(self, id: str = "Google", num_result: int = 5):
        super().__init__(id=id)
        self.num_result = num_result

    def _search(self, query: str = None):
        return [url for url in googlesearch.search(query, num_results=self.num_result)]


class YahooSearch(Search):
    def __init__(self, id: str = "Yahoo"):
        super().__init__(id=id)

    def _search(self, query: str = None):
        return [page.link for page in yahoo_search.search(query).pages]


async def fetch_query_urls(query: str):
    if not query:
        raise ValueError("Empty query string.")

    search_engines = [
        GoogleSearch(num_result=5),
        YahooSearch(),
    ]
    urls = await asyncio.gather(
        *[search_engine.search(query) for search_engine in search_engines]
    )

    return list(chain(*urls))
