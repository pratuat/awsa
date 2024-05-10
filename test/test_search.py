import pytest
import asyncio

from src.search import Search, GoogleSearch, fetch_query_urls

@pytest.mark.unit
def test_search_class():
    ret_value = ["query result"]

    class Klass(Search):
        def _search(self, query):
            return ret_value
        
    assert asyncio.run(Klass(id="id").search("dummy query")) == ret_value


@pytest.mark.unit
def test_google_search_class():
    assert asyncio.run(GoogleSearch().search("climage change"))


@pytest.mark.unit
def test_fetch_query_urls():
    assert fetch_query_urls("climage change")
