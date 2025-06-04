FROM python:3.13-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY uv.lock pyproject.toml ./

RUN apt update && apt install libcairo2 git build-essential gcc -y --no-install-recommends

RUN uv lock --frozen

COPY . .