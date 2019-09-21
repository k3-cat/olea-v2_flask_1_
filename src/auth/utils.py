from flask import abort

from .models import Duck, Lemon


def query_lemon(key: str) -> Lemon:
    lemon: Lemon = Lemon.query.get(key)
    if not lemon:
        abort(401)
    return lemon


def query_duck(pink_id: str) -> Duck:
    duck: Duck = Duck.query.get(pink_id)
    if not duck:
        abort(403)
    return duck
