import os
from flask import Flask
from redis import Redis

app = Flask(__name__)
redis_host = os.getenv('REDIS_HOST', 'redis-service')
app_title = os.getenv('APP_TITLE', 'Default App')
redis = Redis(host=redis_host, port=6379, password=open('/run/secrets/redis_password').read().strip(), decode_responses=True)

@app.route('/')
def index():
    try:
        visits = redis.incr('visits')
        return f"{app_title}: Visited {visits} times."
    except redis.RedisError as e:
        return f"Error connecting to Redis: {str(e)}", 500

@app.route('/health')
def health():
    try:
        redis.ping()
        return 'OK', 200
    except redis.RedisError:
        return 'Redis Unavailable', 503

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
