FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=80 \
    FLASK_DEBUG=false

WORKDIR /app

# Install minimal system dependencies required by image/steganography libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies first for better layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY app.py imageencryptor.py truenas_api.py init.sh ./
COPY templates/ ./templates/
COPY static/ ./static/

RUN mkdir -p /app/static/uploads

EXPOSE 80

CMD ["python", "-u", "app.py"]

