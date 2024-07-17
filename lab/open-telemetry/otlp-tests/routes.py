from flask import Flask
import requests
import sqlite3
from faker import Faker


app = Flask(__name__)

COUNTER = 0


@app.route("/ping")
def ping():
    return "Pong"


@app.route("/requests")
def get_counter():
    COUNTER = +1
    return {"counter": COUNTER}


@app.route("/btc")
def get_btc_price():
    url = "https://api.kucoin.com"
    ticker = requests.get(
        url + "/api/v1/market/orderbook/level1?symbol=BTC-USDT"
    ).json()
    price = ticker.get("data").get("price")
    return {"price": price}


@app.route("/database")
def db_test():
    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()

    fake = Faker()

    cursor.execute(
        """CREATE TABLE IF NOT EXISTS CLIENT
            (ID INTEGER PRIMARY KEY     NOT NULL,
             NAME           TEXT    NOT NULL,
             ADDRESS        CHAR(500));"""
    )

    name = fake.name()
    address = fake.address()
    cursor.execute(f'INSERT INTO CLIENT (NAME,ADDRESS) VALUES ("{name}", "{address}")')
    conn.commit()
    id = cursor.lastrowid

    conn.close()

    return {"id": id}
