from functools import wraps

from flask import g, make_response, request

from exts import db

from .utils import query_lemon


class LemonAuth():
    def __init__(self, scheme='Bearer'):
        self.scheme = scheme.upper()
        res = make_response('Unauthorized Access')
        res.status_code = 401
        res.headers['WWW-Authenticate'] = f'{self.scheme} realm="None"'
        self.error_response = res

    def get_key(self):
        try:
            scheme, lemon = request.headers['Authorization'].split(maxsplit=1)
        except (KeyError, ValueError):
            return None
        if scheme.upper() != self.scheme:
            return None
        return lemon

    def verify_lemon(self, key):
        lemon = query_lemon(key)
        if not lemon:
            return False
        if g.now > lemon.expire:
            db.session.delete(lemon)
            db.session.commit()
            return False
        g.lemon = lemon
        g.pink_id = lemon.pink_id
        return True

    def login_required(self, f):
        @wraps(f)
        def decorated(*args, **kwargs):
            key = self.get_key()
            if not key or not self.verify_lemon(key):
                # Clear TCP receive buffer of any pending data
                request.data
                return self.error_response
            return f(*args, **kwargs)

        return decorated
