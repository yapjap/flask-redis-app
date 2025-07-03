from flask import Flask, request
import redis
import os
import logging
from redis import RedisError

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

redis_client = redis.Redis(
    host=os.getenv('REDIS_HOST', 'redis-service'),
    port=6379,
    password=os.getenv('REDIS_PASSWORD', None),
    decode_responses=True
)

@app.route('/')
def index():
    try:
        count = redis_client.incr('visits')
        logger.info("Incremented visit count")
        app_title = os.getenv('APP_TITLE', 'K8s Flask App')
        return f"{app_title}: Visited {count} times."
    except RedisError as e:
        logger.error(f"Error in index: {e}")
        return "Error", 500

@app.route('/health')
def health():
    try:
        redis_client.ping()
        return 'OK', 200
    except RedisError:
        return 'Redis Unavailable', 503

@app.route('/set_key')
def set_key():
    key = request.args.get('key')
    value = request.args.get('value')
    if not key or not value:
        logger.error("Missing key or value in set_key")
        return "Error: Missing key or value", 400
    try:
        redis_client.set(key, value)
        logger.info(f"Set {key} = {value}")
        return f"Set {key} = {value}\n"
    except RedisError as e:
        logger.error(f"Error in set_key: {e}")
        return "Error", 500

@app.route('/get_key')
def get_key():
    key = request.args.get('key')
    if not key:
        logger.error("Missing key in get_key")
        return "Error: Missing key", 400
    try:
        value = redis_client.get(key)
        logger.info(f"Retrieved {key} = {value}")
        return f"{key} = {value}\n" if value else f"{key} not found\n"
    except RedisError as e:
        logger.error(f"Error in get_key: {e}")
        return "Error", 500

if __name__ == '__main__':
    logger.info(f"FLASK_ENV: {os.getenv('FLASK_ENV')}")
    logger.info(f"REDIS_HOST: {os.getenv('REDIS_HOST')}")
    app.run(host='0.0.0.0', port=5000)


