import os
import json
from flask import Flask
from redis import Redis, RedisError
from prometheus_client import Counter, Histogram, generate_latest, REGISTRY
import socket
import logging

try:
    with open('/tmp/test_write', 'w') as f:
        f.write('test')
    logger.info("Write to /tmp successful")
except OSError as e:
    logger.warning(f"Write to /tmp failed: {e}")

app = Flask(__name__)
redis_host = os.getenv('REDIS_HOST', 'redis-service')
app_title = os.getenv('APP_TITLE', 'Default App')
temp_api_key = os.getenv('TEMP_API_KEY', 'no-api-key')
app.config['DEBUG'] = os.getenv('FLASK_ENV', 'production') == 'development'
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('{"time":"%(asctime)s","level":"%(levelname)s","message":"%(message)s"}'))
logger.addHandler(handler)
logger.info(f"Starting Flask app with instance ID: {os.getpid()}")

try:
    with open('/run/secrets/flask_app_key', 'r') as f:
        app.config['SECRET_KEY'] = f.read().strip()
except FileNotFoundError:
    app.config['SECRET_KEY'] = 'default-secret-key'

visits_counter = Counter('flask_app_visits_total', 'Total visits to the app')
request_latency = Histogram('flask_request_latency_seconds', 'Request latency')

try:
    redis_password = open('/run/secrets/redis_password').read().strip()
    redis = Redis(host=redis_host, port=6379, password=redis_password, decode_responses=True)
except FileNotFoundError:
    logger.error("Redis password secret not found")
    redis = None

@app.route('/')
def index():
    with request_latency.time():
        visits_counter.inc()
        if app.config.get('TESTING') or not redis:
            return f"{app_title}: Visited 1 times."
        try:
            visits = redis.incr('visits')
            return f"{app_title}: Visited {visits} times."
        except RedisError as e:
            return f"Error connecting to Redis: {str(e)}", 500

@app.route('/health')
def health():
    if app.config.get('TESTING') or not redis:
        return 'OK', 200
    try:
        redis.ping()
        return 'OK', 200
    except RedisError:
        return 'Redis Unavailable', 503
