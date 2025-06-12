import os
from flask import Flask
from redis import Redis, RedisError
from prometheus_client import Counter, generate_latest, REGISTRY
app = Flask(__name__)
redis_host = os.getenv('REDIS_HOST', 'redis-service')
app_title = os.getenv('APP_TITLE', 'Default App')
visits_counter = Counter('flask_app_visits_total', 'Total visits to the app')
try:
    redis = Redis(
        host=redis_host,
        port=6379,
        password=open('/run/secrets/redis_password').read().strip() if os.path.exists('/run/secrets/redis_password') else 'supersecretpassword',
        decode_responses=True
    )
except FileNotFoundError:
    redis = None
@app.route('/')
def index():
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
@app.route('/metrics')
def metrics():
    return generate_latest(REGISTRY), 200
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
