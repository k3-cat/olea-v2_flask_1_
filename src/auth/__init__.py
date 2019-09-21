from flask import Blueprint

from .lemon_auth import LemonAuth

__all__ = ['login_required', 'permission_required']

login_required = LemonAuth(scheme='OLEA').login_required

from .duck_permission import DuckPermission
permission_required = DuckPermission().permission_required

auth_bp = Blueprint('auth', __name__)
