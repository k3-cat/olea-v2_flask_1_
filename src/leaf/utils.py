from enums import LeafState

from .errors import AccessDenied, NonExistedObj
from .models import Leaf


def query_leaf(id_: str, europaea: bool = False) -> Leaf:
    leaf: Leaf = Leaf.query.get(id_)
    if not leaf:
        raise NonExistedObj(cls=Leaf)
    if leaf.state == LeafState.finished and not europaea:
        raise AccessDenied(obj=leaf)
    return leaf
