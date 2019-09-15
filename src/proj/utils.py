from .errors import AccessDenied, NonExistedObj, RoleIsTaken
from .models import FreeRole, Proj


def query_proj(id_: str, europaea: bool = False) -> Proj:
    proj: Proj = Proj.query.get(id_)
    if not proj:
        raise NonExistedObj(cls=Proj)
    if proj.finish_at is not None and not europaea:
        raise AccessDenied(obj=proj)
    return proj


def query_freerole(id_: str) -> FreeRole:
    freerole: FreeRole = FreeRole.get(id_)
    if not freerole:
        raise NonExistedObj(cls=FreeRole)
    if freerole.taken:
        raise RoleIsTaken()
    return freerole
