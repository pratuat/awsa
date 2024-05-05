import sys
import asyncio
import googlesearch
import time
import aiohttp
from itertools import chain

from typing import List, Union, Iterable

from abc import ABC, abstractmethod

from bs4 import BeautifulSoup

### Query ###

class Search(ABC):
    async def search (self, query):
        print(f"{self.id} is searching query: {query}")
        result = await asyncio.to_thread(self._search, query)
        print(f"{self.id} has returned query: {query}")

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


async def run_query(query: str):
    if not str:
        raise ValueError("Empty query string.")

    search_engines = [
        GoogleSearch(id="G1", num_result=5),
        # GoogleSearch(id="G2", num_result=10)
    ]
    urls = await asyncio.gather(*[search_engine.search(query) for search_engine in search_engines])

    return list(chain(*urls))


### URL Content ###

async def get_url_doc(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            print(f"URL[{url}]: Response recevied.")
            print(f"URL[{url}]: Response status: {response.status}")

            if response.status == 200:
                return await response.text()
            else:
                return None


async def get_url_docs(urls: List[str]):
    urls = set(urls)
    url_contents = await asyncio.gather(*[get_url_doc(url) for url in urls])

    return [content for content in url_contents if content]


### Extract HTML content

def extract_content(html_page: str):
    pass


def process_html_page(html_pages: List[str]):
    pass

### Main ###

async def main(query):
    urls = await run_query(query)
    html_docs = await get_url_docs(urls)

    print(len(html_docs))

    html_doc = html_docs[0]

    doc = BeautifulSoup(html_doc, 'html.parser')

    import pdb; pdb.set_trace()

if __name__ == "__main__":
    args = sys.argv
    query = args[1]

    asyncio.run(main(query=query))

