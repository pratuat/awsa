import logging
import uuid
import pathlib
import os
import yaml
import asyncio
import aiohttp
import aiofiles
from search import fetch_query_urls
from typing import List
from llm import summarize_html_document, reduce_document_summaries

logger = logging.getLogger()

def create_query_directory(query, urls):
    query_uuid = str(uuid.uuid4())
    dir_path = pathlib.Path(os.getcwd()) / "data" / "docs" / query_uuid

    if dir_path.exists():
        raise FileExistsError("Directory already exists.")

    os.makedirs(dir_path)

    with open(dir_path / "query.yaml", "w") as file:
        data = {
            "query": query,
            "urls": urls
        }
        yaml.dump(data, file)

    return dir_path


async def get_document_summary(file_path: pathlib.Path, url: str, semaphore: asyncio.Semaphore):
    logger.info("Fetch content for url: %s" % (url,))
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                logger.info(f"URL[{url}]: Response recevied.")
                logger.info(f"URL[{url}]: Response status: {response.status}")

                if response.status == 200:
                    doc = await response.text()

                    async with semaphore:
                        async with aiofiles.open(file_path, 'w') as f:
                            await f.write(doc)

                        return await asyncio.to_thread(summarize_html_document, file_path)
    except UnicodeDecodeError as exp:
        logger.error(exp)
        return None


async def get_query_summaries(dir_path: pathlib.Path, urls: List[str]):
    semaphore = asyncio.Semaphore(value=5)

    return await asyncio.gather(*[get_document_summary(dir_path / f"doc_{index}.html", url, semaphore) for index, url in enumerate(urls)])


def query(query: str):
    logger.info("Running query for: %s" % (query,))

    urls = set([url for url in asyncio.run(fetch_query_urls(query=query))])
    logger.info("Retrieved no. of urls: %d" % (len(urls)))

    dir_path = create_query_directory(query, list(urls))
    logger.info("Directory created for query: %s" % (dir_path))

    summaries = list(filter(lambda x: x, asyncio.run(get_query_summaries(dir_path, urls))))
    logger.info("Document summaries generated.")

    if summaries:
        logger.info("="*50)
        logger.info("\n-----\n".join(summaries))
        logger.info("="*50)

        summary = reduce_document_summaries(summaries)
        logger.info("Query summary: %s" % (summary,))

        return summary
    else:
        return "No results found. Try rephrasing the query."
