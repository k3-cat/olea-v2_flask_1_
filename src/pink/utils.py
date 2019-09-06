from .models import Pink
from .errors import PinkNotExist, AccessDenied


def get_pink(id_: str, europaea: bool = False) -> Pink:
    pink: Pink = Pink.query.get(id_)
    if not pink:
        raise PinkNotExist()
    if not pink.active and not europaea:
        raise AccessDenied()
    return pink
