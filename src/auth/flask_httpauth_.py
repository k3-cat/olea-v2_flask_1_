from functools import wraps

from flask import g, make_response, request

from exts import db

from .models import ELemon, Lemon


class HTTPTokenAuth(object):
    def __init__(self, scheme='Bearer', realm=None,
                 verify_token_callback=None):
        self.scheme = scheme.lower()
        self.realm = realm
        self.auth_error_callback = None
        self.verify_token_callback = verify_token_callback

        def default_auth_error():
            return "Unauthorized Access"

        self.error_handler(default_auth_error)

    def error_handler(self, f):
        @wraps(f)
        def decorated(*args, **kwargs):
            res = f(*args, **kwargs)
            res = make_response(res)
            if res.status_code == 200:
                # if user didn't set status code, use 401
                res.status_code = 401
            if 'WWW-Authenticate' not in res.headers.keys():
                res.headers[
                    'WWW-Authenticate'] = f'{self.scheme} realm="{self.realm}"'
            return res

        self.auth_error_callback = decorated
        return decorated

    def get_token(self):
        try:
            scheme, token = request.headers['Authorization'].split(maxsplit=1)
        except (KeyError, ValueError):
            # The Authorization header is either non-exist or has no token
            return None
        if scheme.lower() != self.scheme:
            return None
        return token

    def verify_token(self, f):
        self.verify_token_callback = f
        return f

    def login_required(self, f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = self.get_token()
            if not token or not self.verify_token_callback(token):
                # Clear TCP receive buffer of any pending data
                request.data
                return self.auth_error_callback()
            return f(*args, **kwargs)

        return decorated


def verify_lemon(key):
    lemon: Lemon = Lemon.query.get(key)
    if not lemon:
        return False
    if g.now > lemon.expire:
        db.session.delete(lemon)
        db.session.commit()
        return False
    g.lemon = lemon
    g.pink_id = lemon.pink_id
    return True


def verify_elemon(key):
    elemon: ELemon = ELemon.query.get(key)
    if not elemon:
        return False
    g.elemon = elemon
    g.pink_id = elemon.pink_id
    return True


ta = HTTPTokenAuth(scheme='OLEA', verify_token_callback=verify_lemon)
eta = HTTPTokenAuth(scheme='EUROPAEA', verify_token_callback=verify_lemon)
