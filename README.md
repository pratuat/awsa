# Asynchronous Web Scraping and Analysis

Author: Pratuat Amatya <pratuat@gmail.com>

A demo streamlit app that asynchronously fetch information from internet search engines and summarize the information using LLM model.

## Dependencies

### 1. LLM Model

Download and run a LLM model locally https://ollama.com/.

### 2. Pyenv for installing python

1. Follow installation guide https://github.com/pyenv/pyenv?tab=readme-ov-file#installation to install pyenv.

2. Install python 3.11.7 using command `pyenv install 3.11.7`.

3. Run `pyenv local 3.11.7` to activate the python version.

### 3. Poetry for installing python dependencies

1. Follow installation guide https://python-poetry.org/docs/#installation to install poetry.

2. Run `poetry install` to install all dependencies.

### 4. Run streamlit app

Run `poetry run PYTHONPATH=. streamlit run src/app.py` to start the app server and click on web url displayed in the server log.