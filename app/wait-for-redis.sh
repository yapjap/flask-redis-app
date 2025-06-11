#!/bin/sh
until redis-cli -h redis-service -a $REDIS_PASSWORD ping; do
  echo "Waiting for Redis..."
  sleep 2
done
echo "Redis is up!"
exec python app.py
