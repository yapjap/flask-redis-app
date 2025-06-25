FROM python:3.9-slim
WORKDIR /app
RUN apt-get update && apt-get install -y redis-tools curl iputils-ping && \
    apt-get clean && rm -rf /var/lib/apt/lists/* && \
    useradd -m -u 1000 appuser
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir flask gunicorn && \
    chown -R appuser:appuser /app
COPY app/ .
USER appuser
ENV PATH="/home/appuser/.local/bin:$PATH"
# Ensure flask/gunicorn is in PATH for appuser
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
