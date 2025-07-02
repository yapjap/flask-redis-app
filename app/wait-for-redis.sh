#!/bin/sh
#until redis-cli -h redis-service -a $REDIS_PASSWORD ping; do
#  echo "Waiting for Redis..."
#  sleep 2
#done
#echo "Redis is up!"

#!/bin/bash
# wait-for-redis.sh

# Wait for Redis to be available
echo "Waiting for Redis at $REDIS_HOST:6379..."
until redis-cli -h $REDIS_HOST -p 6379 ping &> /dev/null; do
  echo "Redis not ready, retrying in 5 seconds..."
  sleep 5
done
echo "Redis is up!"
