FROM postgres:latest

# Install Python and venv
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3-full \
    python3-venv \
    python3-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Create and activate virtual environment
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Copy requirements file
COPY requirements.txt .

# Install Python packages in virtual environment
RUN pip install --no-cache-dir -r requirements.txt

# Copy initialization SQL script
COPY init.sql /docker-entrypoint-initdb.d/

# Copy your Python scripts
COPY scripts/ /app/scripts/

# Set working directory
WORKDIR /app

# Make sure we use the virtualenv
ENV PYTHONPATH="${PYTHONPATH}:/app"

# Ensure PostgreSQL starts first, then run Python script
CMD ["python", "scripts/main_postgre.py"]
