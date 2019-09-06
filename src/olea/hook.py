import datetime

from flask import g


def add_timestamp():
    g.now = datetime.datetime.utcnow()


def hook_hooks(app):
    app.before_request(add_timestamp)
