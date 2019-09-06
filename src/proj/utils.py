from .models import Proj
from .errors import ProjNotExist, AccessDenied


def get_proj(id_: str, europaea: bool = False) -> Proj:
    proj: Proj = Proj.query.get(id_)
    if not proj:
        raise ProjNotExist()
    if proj.finish_at is not None and not europaea:
        raise AccessDenied()
    return proj
