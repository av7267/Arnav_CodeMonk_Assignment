FROM python:3.10-alpine

# Prevent Python from creating .pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# Ensure logs are displayed immediately
ENV PYTHONUNBUFFERED=1

# Set application working directory
WORKDIR /app

# Install required system dependencies
RUN apk update && apk add --no-cache \
    postgresql-dev \
    gcc \
    python3-dev \
    musl-dev

# Install Python dependencies
COPY requirements.txt /app/

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy project files into the container
COPY . /app/