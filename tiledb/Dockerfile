# Use official Python image with a stable tag
FROM python:3.9

# Install system dependencies (if needed)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY tiledb/requirements.txt .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy common utils
COPY common/utils /app/utils/

# Copy your Python scripts
COPY tiledb/scripts/ /app/scripts/

# Set working directory
WORKDIR /app

# Set Python path
ENV PYTHONPATH="${PYTHONPATH}:/app"

# Run your script
CMD ["python", "scripts/main_tiledb.py"]
