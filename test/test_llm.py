import pytest
import pathlib

from src.llm import summarize_html_document, reduce_document_summaries


@pytest.mark.unit
@pytest.mark.parametrize("data_dir,", [pathlib.Path("test/data")])
def test_summarize_html_document(data_dir):

    summaries = [
        summarize_html_document(file_path) for file_path in data_dir.rglob("*.html")
    ]
    assert summaries

    summary = reduce_document_summaries(summaries)
    assert summary
