#!/bin/bash
# Remove volumes older than retention policy
docker volume ls --format "{{.Name}} {{.Labels}}" | grep "com.example.retention=7d" | while read -r volume labels; do
  created=$(docker volume inspect "$volume" --format '{{.CreatedAt}}' | date -d - +%s)
  threshold=$(date -d '7 days ago' +%s)
  if [ "$created" -lt "$threshold" ]; then
    docker volume rm "$volume"
  fi
done
