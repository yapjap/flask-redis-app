FROM python:3.9-slim
WORKDIR /app
RUN apt-get update && apt-get install -y redis-tools curl iputils-ping dnsutils && \
    apt-get clean && rm -rf /var/lib/apt/lists/* && \
    useradd -m -u 1000 appuser
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir flask gunicorn prometheus_client && \
    chown -R appuser:appuser /app
COPY app/ .
COPY app/health_check.sh /app/health_check.sh
COPY redis_health.sh /redis_health.sh
RUN chmod +x /app/health_check.sh /redis_health.sh
USER appuser
ENV PATH="/home/appuser/.local/bin:$PATH"
#CMD ["./wait-for-redis.sh"]
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
