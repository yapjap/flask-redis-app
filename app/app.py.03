import logging
import os
from flask import Flask
import redis
from redis.exceptions import RedisError

# Configure logging
log_level = os.getenv('LOG_LEVEL', 'INFO')
logging.basicConfig(level=getattr(logging, log_level), format='{"time":"%(asctime)s","level":"%(levelname)s","message":"%(message)s"}')
logger = logging.getLogger(__name__)
logger.info(f"Set log level to {log_level}")

app = Flask(__name__)

# Initialize Redis client (no password, using redis-service from Kubernetes)
try:
    redis_host = os.getenv('REDIS_HOST', 'redis-service')
    r = redis.Redis(host=redis_host, port=6379, decode_responses=True)
    r.ping()
    logger.info("Connected to Redis")
except redis.ConnectionError as e:
    logger.error(f"Failed to connect to Redis: {e}")
    raise

@app.route('/')
def index():
    try:
        count = r.incr('visits')
        logger.info("Incremented visit count")
        app_title = os.getenv('APP_TITLE', 'K8s Flask App')
        return f"{app_title}: Visited {count} times."
    except RedisError as e:
        logger.error(f"Error in index: {e}")
        return "Error", 500

@app.route('/health')
def health():
    try:
        r.ping()
        return 'OK', 200
    except RedisError:
        return 'Redis Unavailable', 503

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
