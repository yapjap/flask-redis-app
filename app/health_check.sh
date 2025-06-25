#!/bin/bash
# Check Flask app and Redis connectivity
if ! curl -f http://localhost:5000/health >/dev/null; then
  echo "Flask health endpoint failed"
  exit 1
fi
if ! redis-cli -h redis-service -p 6379 -a "$REDIS_PASSWORD" ping | grep -q PONG; then
  echo "Redis connectivity failed"
  exit 1
fi
exit 0
