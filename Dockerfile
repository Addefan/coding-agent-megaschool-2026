FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app

COPY pyproject.toml uv.lock ./

# TODO: install dependencies to the global interpreter instead of creating .venv
RUN uv sync --frozen

COPY . .

ENTRYPOINT ["uv", "run", "main.py"]
CMD ["--help"]
