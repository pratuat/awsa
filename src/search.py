import logging
import asyncio
import googlesearch
from itertools import chain
from abc import abstractmethod, ABC

logger = logging.getLogger()

class Search(ABC):
    async def search (self, query):
        logger.info(f"{self.id} is searching query: {query}")
        result = await asyncio.to_thread(self._search, query)
        logger.info(f"{self.id} has returned query: {query}")

        return result

    @abstractmethod
    def _search(self, query):
        pass

class GoogleSearch(Search):
    def __init__(self,id: str = None, num_result: int = 5):
        self.id = id
        self.num_result = num_result

    def _search(self, query: str = None):
        return [url for url in googlesearch.search(query, num_results=self.num_result)]


async def fetch_query_urls(query: str):
    if not str:
        raise ValueError("Empty query string.")

    search_engines = [
        GoogleSearch(id="Google", num_result=10),
    ]
    urls = await asyncio.gather(*[search_engine.search(query) for search_engine in search_engines])

    return list(chain(*urls))
