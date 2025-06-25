import logging
import os
from flask import Flask
import redis as redis_client  # Explicit alias to avoid confusion
from redis.exceptions import RedisError
from prometheus_client import Gauge
health_status = Gauge('flask_app_health_status', 'Health check status')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('{"time":"%(asctime)s","level":"%(levelname)s","message":"%(message)s"}'))
logger.addHandler(handler)

app = Flask(__name__)

try:
    redis_host = os.environ.get('REDIS_HOST', 'localhost')
    redis_password = os.environ.get('REDIS_PASSWORD', '')
#    redis_client = Redis(host=redis_host, port=6379, password=redis_password)
#    redis_client.ping()
    # Initialize Redis client (adjust host/port/password as per your setup)
    redis = redis_client.Redis(host=redis_host, port=6379, password=redis_password, decode_responses=True)
    redis.ping()
    logger.info("Connected to Redis")
except redis.exceptions.ConnectionError as e:
    logger.error(f"Failed to connect to Redis: {e}")
    raise

@app.route('/')
def index():
    try:
        count = redis_client.incr('visits')
        logger.info("Incremented visit count")
        with open('/tmp/test.txt', 'w') as f:
            f.write('Test write')
        logger.info("Write to /tmp successful")
        return f"App from .env: Visited {count} times."
    except Exception as e:
        logger.error(f"Error in index: {e}")
        return "Error", 500

@app.route('/health')
def health():
    if app.config.get('TESTING') or not redis:
        health_status.set(1)
        return 'OK', 200
    try:
        redis.ping()
        health_status.set(1)
        return 'OK', 200
    except RedisError:
        health_status.set(0)
        return 'Redis Unavailable', 503
