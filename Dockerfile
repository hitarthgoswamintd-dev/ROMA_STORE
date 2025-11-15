# ROMA Shopping Agent - Dockerized
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Install dependencies first (better cache)
COPY requirements.txt ./
RUN python -m pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy app
COPY . .

# Expose Flask port
ENV FLASK_ENV=production
ENV FLASK_PORT=5000
EXPOSE 5000

# Run the server
CMD ["python", "app.py"]
