#!/bin/bash
# Check Redis memory usage and connectivity
if ! redis-cli -h localhost -p 6379 -a "$REDIS_PASSWORD" ping | grep -q PONG; then
  echo "Redis authentication or connectivity failed"
  exit 1
fi
MEMORY=$(redis-cli -h localhost -p 6379 -a "$REDIS_PASSWORD" INFO MEMORY | grep used_memory: | cut -d: -f2 | tr -d '\r\n')

if [[ "$MEMORY" =~ ^[0-9]+$ ]] && [ "$MEMORY" -lt 100000000 ]; then
  exit 0
else
  echo "Redis memory check failed: MEMORY=$MEMORY"
  exit 1
fi
