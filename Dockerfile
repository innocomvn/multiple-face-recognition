# Face Recognition Attendance System - Docker Image

FROM python:3.8-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    libgtk-3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Create necessary directories
RUN mkdir -p "Training images" "Customer images"

# Expose port
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=app_improved.py
ENV PYTHONUNBUFFERED=1

# Run the application
CMD ["python", "app_improved.py"]
