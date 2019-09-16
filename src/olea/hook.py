import datetime

from flask import g

from exts import db


def hook_hooks(app):
    @app.before_request
    def add_timestamp():
        g.now = datetime.datetime.utcnow()

    @app.after_request
    def auto_commit(response):
        if not g.read_only:
            db.session.commit()
        return response
