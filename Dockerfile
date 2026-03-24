# Use slim Python 3.12 base image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        postgresql-client \
        netcat-openbsd \
        curl \
        && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir mlflow boto3 psycopg2-binary

# Copy your workspace (optional, for MLflow projects / notebooks)
# COPY ./workspace /app/workspace

# Set default command to a wait-for script
COPY wait-and-run.sh /usr/local/bin/wait-and-run.sh
RUN chmod +x /usr/local/bin/wait-and-run.sh

CMD ["/usr/local/bin/wait-and-run.sh"]