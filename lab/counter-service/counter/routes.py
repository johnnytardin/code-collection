from flask import Flask
import redis

from .connection import pool


app = Flask(__name__)


@app.route("/ping")
def ping():
    return "Pong"


@app.route("/")
def get_counter():
    r = redis.Redis(connection_pool=pool)
    request_count = r.get("count")
    if request_count:
        new_count = int(request_count) + 1
    else:
        new_count = 1
    r.set("count", new_count)
    return {"counter": new_count}
