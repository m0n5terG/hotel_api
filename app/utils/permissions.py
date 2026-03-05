from flask import abort
from flask_jwt_extended import get_jwt_identity

from ..models import User

def admin_required():
    """Get the current user and ensure they are admin, abort 403 if not."""
    user = User.query.get(int(get_jwt_identity()))
    if not user or not user.is_admin:
        abort(403, description="Admin access required")
    return user
