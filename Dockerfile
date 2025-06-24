# Build stage
FROM python:3.9-slim AS builder
WORKDIR /app
COPY app/requirements.txt .
RUN apt-get update && apt-get install -y curl redis-tools iputils-ping && pip install --user -r requirements.txt && apt-get clean && rm -rf /var/lib/apt/lists/*
# Final stage
FROM python:3.9-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY app/ .
ENV PATH=/root/.local/bin:$PATH
CMD ["./wait-for-redis.sh"]
