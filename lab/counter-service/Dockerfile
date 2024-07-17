FROM python:3.9.1-slim-buster

ENV FLASK_APP=app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock /app/
RUN poetry config virtualenvs.create false && poetry install --no-dev

COPY . /app

ENTRYPOINT ["python", "-m", "counter"]
