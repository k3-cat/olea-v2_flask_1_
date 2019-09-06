from enums import LeafState

from .errors import AccessDenied, LeafNotExist
from .models import Leaf


def get_leaf(id_: str, europaea: bool = False) -> Leaf:
    leaf: Leaf = Leaf.query.get(id_)
    if not leaf:
        raise LeafNotExist()
    if leaf.state == LeafState.finished and not europaea:
        raise AccessDenied()
    return leaf
