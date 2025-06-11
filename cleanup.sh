#!/bin/bash
echo "Stopping and removing Flask app containers..."
docker compose --profile $1 down
echo "Removing unused volumes..."
docker volume prune -f
echo "Removing unused networks..."
docker network prune -f
echo "Removing unused images..."
docker image prune -f
echo "Cleanup complete!"
