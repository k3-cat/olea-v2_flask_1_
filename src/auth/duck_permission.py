from functools import wraps

from flask import g, make_response, request

from . import login_required
from .utils import query_duck


class DuckPermission():
    def __init__(self):
        res = make_response('Access Denied')
        res.status_code = 403
        self.error_response = res

    def permission_required(self, perm):
        def real_decorator(f):
            @wraps(f)
            def decorated(*args, **kwargs):
                duck = query_duck(g.pink_id)

                if not duck.has_perm(perm) or not duck.check_signature():
                    # Clear TCP receive buffer of any pending data
                    request.data
                    return self.error_response
                # TODO: log here
                return f(*args, **kwargs)

            return login_required(decorated)

        return real_decorator
