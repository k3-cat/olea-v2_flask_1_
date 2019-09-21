from functools import wraps

from flask import abort, g, request

from exts import db

from .utils import query_lemon


class LemonAuth():
    def __init__(self, scheme='Bearer'):
        self.scheme = scheme.upper()

    def get_key(self):
        try:
            scheme, key = request.headers['Authorization'].split(maxsplit=1)
        except (KeyError, ValueError):
            abort(401)
        if scheme.upper() != self.scheme:
            abort(401)
        return key

    def verify_lemon(self, lemon):
        if g.now > lemon.expire:
            db.session.delete(lemon)
            db.session.commit()
            abort(401)
        g.pink_id = lemon.pink_id
        return True

    def login_required(self, f):
        @wraps(f)
        def decorated(*args, **kwargs):
            key = self.get_key()
            self.verify_lemon(query_lemon(key))
            return f(*args, **kwargs)

        return decorated
