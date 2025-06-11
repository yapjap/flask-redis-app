#!/bin/sh
REDIS_PASSWORD=$(cat /run/secrets/redis_password)
exec redis-server --requirepass "$REDIS_PASSWORD"
