from flask import Blueprint

from .duck_permission import DuckPermission
from .lemon_auth import LemonAuth

__all__ = ['login_required', 'permission_required']

login_required = LemonAuth(scheme='OLEA').login_required
permission_required = DuckPermission().permission_required

auth_bp = Blueprint('auth', __name__)
