#!/usr/bin/env bash
echo "RUNNING product Backend..."

echo "Waiting for product Backend POSTGRESQL Database..."
while ! nc -z ${POSTGRES_HOST} ${POSTGRES_PORT}; do
  echo "Waiting for PostgreSQL..."
  sleep 2
done
echo "Connected to product Backend POSTGRESQL Database"

python /home/app/manage.py makemigrations --noinput
python /home/app/manage.py migrate --noinput

if [ $? -ne 0 ]; then
  echo "Migration product Backend POSTGRESQL DB failed." >&2
  exit 1
fi

# echo "Creating superuser if not exists..."
# python /home/app/manage.py shell < /home/app/scripts/create_superuser.py


echo "Starting Gunicorn for wrench ..."

exec gunicorn config.wsgi:application \
  --name product-gunicorn \
  --bind 0.0.0.0:${APP_PORT:-8000} \
  --workers ${GUNICORN_WORKER_NUMBER} \
  --pythonpath "/home/app/" \
  --log-level=info \
  --log-file=- \
  --timeout ${GUNICORN_TIMEOUT} \
  --reload

# tail -f /dev/null

