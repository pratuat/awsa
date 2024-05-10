import pytest
import pathlib

from src.query import (
    create_query_directory
)

@pytest.mark.unit
@pytest.mark.parametrize("query,urls", [["dummy query", ["url_1", "url_2"]]])
def test_create_query_directory(query, urls):
    dir_path = create_query_directory(query, urls)
    assert pathlib.Path(dir_path).exists()
    assert pathlib.Path(dir_path / "query.yaml").exists()
