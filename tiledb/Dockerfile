# Use official Python image with a stable tag
FROM python:3.9

# Install system dependencies (if needed)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy your Python scripts
COPY scripts/ /app/scripts/

# Set working directory
WORKDIR /app

# Run your script
CMD ["python", "scripts/main_tiledb.py"]