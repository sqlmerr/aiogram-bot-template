FROM python:3.11-slim

RUN curl -sSL https://install.python-poetry.org | python3 -

COPY poetry.lock pyproject.toml /code/
RUN poetry install

COPY . /app
WORKDIR /app

CMD ["python3", "-m", "bot"]