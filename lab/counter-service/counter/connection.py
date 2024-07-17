import redis
from decouple import config


REDIS_HOST = config("REDIS_HOST", "redis")
REDIS_PORT = config("REDIS_PORT", 6379)


pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=0)
