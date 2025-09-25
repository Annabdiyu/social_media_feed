# ---- Base image ----
FROM python:3.12-slim

# Set work directory
WORKDIR /app

# Prevent Python from writing .pyc files & enable unbuffered logs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install OS dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev gcc --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project code
COPY . .

# Default run command (gunicorn for production; can override)
CMD ["gunicorn", "backend.wsgi:application", "--bind", "0.0.0.0:8000"]
