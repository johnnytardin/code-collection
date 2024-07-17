from postgres import Postgres
from flask import Flask
from gevent.pywsgi import WSGIServer
from requests import get
from decouple import config


DB_USER = config("DB_USER", "test")
DB_PASSWD = config("DB_PASSWD", "test")
DB_NAME = config("DB_NAME", "test")
DB_HOST = config("DB_HOST", "postgres")
DB_PORT = config("DB_PORT", 5432)
ENVIRONMENT = config("ENVIRONMENT", "development")
PORT = config("PORT", 8080)
DEBUG = config("DEBUG", True)


db = Postgres(f"postgres://{DB_USER}:{DB_PASSWD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
app = Flask(__name__)


@app.route("/ping")
def ping():
    return "Pong"


@app.route("/http")
def get_http():
    r = get("http://httpbin.org/get")
    return {"status": r.json()}


@app.route("/https")
def get_https():
    r = get("https://gorest.co.in/public/v1/users")
    return {"status": r.json()}


@app.route("/postgres")
def get_postgres():
    query_insert = "INSERT INTO COUNTER VALUES (1)"
    query_select = "SELECT COUNT(*) FROM counter"
    db.run(query_insert)
    r = db.one(query_select)
    return {"counter": r}


if __name__ == "__main__":
    if ENVIRONMENT == "production":
        http_server = WSGIServer((PORT, 8080), app)
        http_server.serve_forever()
    else:
        app.run(debug=DEBUG, host="0.0.0.0", port=PORT)
