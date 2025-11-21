FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# uv
RUN pip install --no-cache-dir uv

COPY pyproject.toml ./
COPY uv.lock ./

RUN uv sync

COPY ./src ./src

ENTRYPOINT []
