import logging
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from langchain_community.document_loaders import UnstructuredHTMLLoader
from unstructured.cleaners.core import remove_punctuation, clean, clean_extra_whitespace
import asyncio
import pathlib


logger = logging.getLogger()

llm_model = Ollama(model="llama3")

summarize_document_prompt = PromptTemplate.from_template(
    """
    Give a short summary of the text below.

    {document}
    """
)

reduce_documenet_summaries_prompt = PromptTemplate.from_template(
    """
    The following is set of summaries:
    {docs}
    Take these and distill it into a final, consolidated summary (into a one paragram summary text without bulletpoints) of the main themes.
    """
)


def summarize_html_document(file_path: pathlib.Path):
    logger.info("Summarizing document: %s" % (file_path,))
    try:
        content = UnstructuredHTMLLoader(
            file_path,
            post_processors=[clean, remove_punctuation, clean_extra_whitespace],
        ).load()

        return llm_model.invoke(summarize_document_prompt.format(document=content))
    except:
        return None


def reduce_document_summaries(summaries):
    try:
        prompt = reduce_documenet_summaries_prompt.format(
            docs="\n-----Document------\n".join(summaries)
        )

        return llm_model.invoke(prompt)
    except:
        return None
