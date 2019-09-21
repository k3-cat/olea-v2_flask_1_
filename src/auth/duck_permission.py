import base64
import datetime
from functools import wraps

from flask import g, request

from . import login_required
from .errors import InvalidEuropaeaRequet
from .utils import query_duck


class DuckPermission():
    def permission_required(self, perm):
        def real_decorator(f):
            @wraps(f)
            def decorated(*args, **kwargs):
                duck = query_duck(g.pink_id)
                try:
                    signature = base64.decodebytes(
                        request.headers['signature'])
                    timestamp = datetime.datetime.fromisoformat(
                        request.headers['timestamp'])
                except (KeyError, ValueError):
                    raise InvalidEuropaeaRequet()
                if not g.now - datetime.timedelta(
                        seconds=5) <= timestamp < g.now:
                    raise InvalidEuropaeaRequet()
                duck.has_perm(perm)
                duck.check_signature(
                    signature=signature,
                    content=f'{timestamp.isoformat()}|{request.get_json()}'.
                    encode('utf-8'))
                # TODO: log here
                return f(*args, **kwargs)

            return login_required(decorated)

        return real_decorator
