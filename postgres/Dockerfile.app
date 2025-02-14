FROM python:3.12-slim

# Install required system packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements file
COPY postgres/requirements.txt .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy common utils
COPY common/utils /app/utils/

# Copy your Python scripts
COPY postgres/scripts/ /app/scripts/

# Copy the entrypoint script
COPY postgres/scripts/wait-for-postgres.py /app/wait-for-postgres.py

# Set Python path
ENV PYTHONPATH="${PYTHONPATH}:/app"

# Run with connection retry logic
CMD ["python", "/app/wait-for-postgres.py"]
