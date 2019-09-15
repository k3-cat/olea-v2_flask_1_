from .errors import AccessDenied, NonExistedObj
from .models import Pink


def query_pink(id_: str, europaea: bool = False) -> Pink:
    pink: Pink = Pink.query.get(id_)
    if not pink:
        raise NonExistedObj(cls=Pink)
    if not pink.active and not europaea:
        raise AccessDenied(obj=pink)
    return pink
