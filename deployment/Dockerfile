# Multi-stage Dockerfile with environment validation and flexible runtime
FROM python:3.11-slim AS base

# Set environment variables for all stages
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

# Install system dependencies (including curl for health checks)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    procps \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install additional production dependencies
RUN pip install gunicorn python-dotenv

# ============== DEVELOPMENT STAGE ==============
FROM base AS development

# Create a non-root user first
RUN adduser --disabled-password --gecos '' appuser

# Copy project files and change ownership in one step
COPY --chown=appuser:appuser . .
USER appuser

# Development health check (more frequent for faster feedback)
HEALTHCHECK --interval=10s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f -s http://localhost:$PORT/health/ || exit 1

# Start Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]

# ============== PRODUCTION STAGE ==============
FROM base AS production

# Create a non-root user first
RUN adduser --disabled-password --gecos '' appuser

# Create staticfiles directory with proper ownership before switching to appuser
RUN mkdir -p /app/staticfiles && chown -R appuser:appuser /app/staticfiles

# Copy project files and change ownership in one step
COPY --chown=appuser:appuser . .
USER appuser

# Collect static files
RUN python manage.py collectstatic --noinput

# Production health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=60s --retries=3 \
    CMD curl -f -s http://localhost:$PORT/health/ || exit 1

# Expose port
EXPOSE 8080

# Start production server
CMD ["gunicorn", "--bind", ":8080", "--workers", "1", "--threads", "8", "--timeout", "0", "--access-logfile", "-", "--access-logformat", "%(h)s %(l)s %(u)s %(t)s \"%(r)s\" %(s)s %(b)s \"%(f)s\" \"%(a)s\"", "cabana_project.wsgi:application"]