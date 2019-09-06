from flask import Blueprint
from .flask_httpauth_ import ta, eta

__all__ = ['ta', 'eta']
auth_bp = Blueprint('auth', __name__)
