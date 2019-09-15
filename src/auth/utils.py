from .models import Duck, Lemon


def query_lemon(key: str) -> Lemon:
    lemon: Lemon = Lemon.query.get(key)
    if not lemon:
        return
    return lemon


def query_duck(pink_id: str, europaea: bool = False) -> Duck:
    duck: Duck = Duck.query.get(pink_id)
    if not duck and europaea:
        duck = Duck(pink_id)
    return duck
