#!/bin/bash
set -e

# Wait for Postgres
echo "Waiting for Postgres..."
until pg_isready -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -U "$POSTGRES_USER"; do
  sleep 1
done
echo "Postgres is ready!"

# Wait for MinIO
echo "Waiting for MinIO..."
until nc -z "$MINIO_HOST" "$MINIO_PORT"; do
  sleep 1
done
echo "MinIO is ready!"

# Start MLflow server
echo "Starting MLflow server..."
exec mlflow server \
  --backend-store-uri "$MLFLOW_TRACKING_URI" \
  --default-artifact-root "$ARTIFACT_ROOT" \
  --host 0.0.0.0 \
  --port 5000