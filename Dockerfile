FROM python:3.9-slim
WORKDIR /app
COPY app/ .
RUN apt-get update && apt-get install -y curl redis-tools iputils-ping && pip install -r requirements.txt && apt-get clean && rm -rf /var/lib/apt/lists/*
CMD ["./wait-for-redis.sh"]
