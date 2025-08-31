FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

WORKDIR /app/server

# Copy pyproject.toml and poetry.lock from the server folder
COPY server/pyproject.toml server/poetry.lock* /app/server/

# Install poetry
RUN pip install --no-cache-dir poetry==1.8.3
RUN poetry config virtualenvs.create false
RUN poetry install --no-root --no-interaction --no-ansi

# Copy the rest of the server code
COPY server /app/server

EXPOSE 8000

CMD ["uvicorn", "server.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
