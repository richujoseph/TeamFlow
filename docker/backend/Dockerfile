# =============================================================================
# TeamFlow EPMS — Backend Dockerfile
# =============================================================================
# Multi-stage build for the Django backend.
#
# Stage 1 (base): Install Python dependencies
# Stage 2 (app):  Copy source code, create non-root user, configure entrypoint
#
# Development: docker compose runs with bind mount + runserver
# Production:  gunicorn via CMD
# =============================================================================

# ---------------------------------------------------------------------------
# Stage 1: Base — install system deps and Python packages
# ---------------------------------------------------------------------------
FROM python:3.14-slim AS base

# Prevent Python from writing .pyc files and enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install system dependencies required for psycopg (PostgreSQL adapter)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        libpq-dev \
        && rm -rf /var/lib/apt/lists/*

# Create working directory
WORKDIR /app

# Install Python dependencies
COPY requirements/ requirements/
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements/dev.txt

# ---------------------------------------------------------------------------
# Stage 2: Application — copy code and configure runtime
# ---------------------------------------------------------------------------
FROM base AS app

# Create a non-root user for security
RUN groupadd --gid 1000 teamflow && \
    useradd --uid 1000 --gid teamflow --shell /bin/bash --create-home teamflow

# Copy application source code
COPY . /app/

# Copy and set permissions on entrypoint script
COPY ../docker/backend/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Create directories for static and media files
RUN mkdir -p /app/staticfiles /app/media && \
    chown -R teamflow:teamflow /app

# Switch to non-root user
USER teamflow

# Expose the Django dev server port
EXPOSE 8000

# Use entrypoint for startup tasks (wait for DB, run migrations in dev)
ENTRYPOINT ["/entrypoint.sh"]

# Default command: Gunicorn for production
# Overridden by docker-compose for development (runserver)
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
