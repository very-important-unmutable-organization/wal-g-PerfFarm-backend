FROM python:3.10-slim-buster

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV POETRY_VERSION=1.1.12
ARG ENV

RUN mkdir -p /src/

RUN apt-get update && apt-get install -y --no-install-recommends libgdal-dev \
    && apt-get autoclean && apt-get autoremove \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*  \
    && pip install "poetry==$POETRY_VERSION" \
    && poetry config virtualenvs.create false

COPY poetry.lock poetry.lock
COPY pyproject.toml pyproject.toml
COPY setup.cfg setup.cfg

RUN poetry install $(if test "$ENV" = prod; then echo "--no-dev"; fi)

COPY src/ /src/
WORKDIR /src/

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.7.3/wait /wait
RUN chmod +x /wait
