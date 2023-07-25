FROM python:3.11-buster

# Pythonの標準出力のバッファリングを無効
ENV PYTHONUNBUFFERED 1

WORKDIR /src

# pipを使ってpoetryをインストール
RUN pip install poetry

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=0 \
    POETRY_VIRTUALENVS_CREATE=0 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

# poetryでライブラリをインストール (pyproject.tomlが既にある場合)
RUN if [ -f pyproject.toml ]; then poetry install --without dev && rm -rf $POETRY_CACHE_DIR; fi

COPY . /src
ENV PYTHONPATH=/src
