#!/bin/sh

echo "Waiting for PostgreSQL..."

while ! nc -z db 5432; do
  sleep 0.1
done

echo "PostgreSQL started"

echo "Making new migrations..."
python manage.py makemigrations

echo "Applying database migrations..."
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting server..."
exec "$@"