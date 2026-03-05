from flask import Blueprint, request
from werkzeug.security import generate_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..extensions import db
from ..models import User, Hotel, HotelComment
from ..services.supabase_storage import upload_avatar

profile_bp = Blueprint("profile", __name__)


# ==========================================
# UPDATE MY PROFILE
# ==========================================

@profile_bp.patch("/me")
@jwt_required()
def update_my_profile():

    user = User.query.get_or_404(int(get_jwt_identity()))

    name = request.form.get("name")
    shortname = request.form.get("shortname")
    password = request.form.get("password")
    photo = request.files.get("photo")

    # -------------------
    # Update name
    # -------------------
    if name is not None:
        name = name.strip()

        if name == "":
            return {"error": "Name cannot be empty"}, 400

        if len(name) > 100:
            return {"error": "Name too long"}, 400

        user.name = name

    # -------------------
    # Update shortname (Crew AKA)
    # -------------------
    if shortname is not None:
        shortname = shortname.strip()

        if shortname == "":
            user.shortname = None
        else:
            if len(shortname) > 50:
                return {"error": "Shortname too long"}, 400

            user.shortname = shortname

    # -------------------
    # Update password
    # -------------------
    if password:
        password = password.strip()

        if len(password) < 6:
            return {"error": "Password must be at least 6 characters"}, 400

        user.password_hash = generate_password_hash(password)

    # -------------------
    # Update photo (Supabase)
    # -------------------
    if photo:
        url = upload_avatar(photo)
        user.photo = url

    db.session.commit()

    return {
        "message": "Profile updated successfully",
        "profile": {
            "staff_id": user.staff_id,
            "name": user.name,
            "shortname": user.shortname,
            "photo": user.photo
        }
    }, 200


# ==========================================
# GET MY PROFILE
# ==========================================

@profile_bp.get("/me")
@jwt_required()
def get_my_profile():

    user = User.query.get_or_404(int(get_jwt_identity()))

    return {
        "user_id": user.id,
        "staff_id": user.staff_id,
        "name": user.name,
        "shortname": user.shortname,
        "photo": user.photo,
        "approved": user.approved,
        "is_admin": user.is_admin,

        # profile stats
        "comments_count":
            HotelComment.query
            .filter_by(user_id=user.id)
            .count(),

        "hotels_added":
            Hotel.query
            .filter_by(created_by=user.id)
            .count()
    }, 200