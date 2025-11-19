FROM python:3.13-slim

WORKDIR /mcp-auth

ENV POETRY_VERSION=2.2.1 \
    POETRY_VIRTUALENVS_IN_PROJECT=true

ENV PATH="/mcp-auth/.venv/bin:$PATH"

RUN pip install "poetry==${POETRY_VERSION}"

COPY poetry.lock pyproject.toml ./
RUN poetry install --only main

COPY .env ./
COPY app/ app/

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
