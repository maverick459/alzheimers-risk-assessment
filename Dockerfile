# ---- Base image for all stages ----
FROM python:3.11-slim-bookworm AS base
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VERSION=1.8.2 \
    POETRY_VIRTUALENVS_IN_PROJECT=true

# ---- Builder stage ----
FROM base AS builder

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /app

# Copy only dependency files for better caching
COPY pyproject.toml poetry.lock* ./

# Install dependencies (production only)
RUN poetry install --no-interaction --no-ansi --no-root --only main

# Copy application code (including templates)
COPY . .

# ---- Runtime stage ----
FROM base AS runtime

# Create a non-root user
RUN useradd -m appuser

WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /app/.venv /app/.venv
# Copy application code from builder
COPY --from=builder /app /app

# Set PATH to use Poetry's virtualenv
ENV PATH="/app/.venv/bin:$PATH"

# Expose Flask port
EXPOSE 5000

# Switch to non-root user
USER appuser

# Healthcheck (adjust endpoint as needed)
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:5000/ || exit 1

# Use Gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
