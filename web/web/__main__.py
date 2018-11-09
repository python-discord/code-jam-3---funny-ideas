#!/usr/bin/env python3

import os

import redis
from flask import Flask


REDIS_OPTS = {
    "host": "localhost",
    "port": 6379,
    "db": 0,
    "password": os.environ.get("REDIS_PWD"),
    "decode_responses": True  # By default all methods return bytes() but we don't want that
}

red = redis.Redis(**REDIS_OPTS)

from web.routes import api # noqa

app = Flask(__name__)
app.register_blueprint(api.app, url_prefix="/api")
