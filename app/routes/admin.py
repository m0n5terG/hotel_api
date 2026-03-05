from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from ..extensions import db
from ..models import User, Hotel
from ..utils.permissions import admin_required

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.get("/users")
@jwt_required()
def get_all_users():
    admin_required()  # will abort if not admin
    
    users = User.query.order_by(User.id).all()
    
    return [
        {
            "id": u.id,
            "staff_id": u.staff_id,
            "name": u.name,
            "shortname": u.shortname,
            "approved": u.approved,
            "is_admin": u.is_admin
        }
        for u in users
    ], 200


@admin_bp.get("/users/pending")
@jwt_required()
def get_pending_users():
    admin_required()

    users = User.query.filter_by(approved=False).all()

    return [
        {"id": u.id, "staff_id": u.staff_id}
        for u in users
    ], 200


@admin_bp.patch("/users/<int:user_id>/approve")
@jwt_required()
def approve_user(user_id):
    admin_required()

    user = User.query.get_or_404(user_id)
    user.approved = True

    db.session.commit()

    return {"message": "User approved"}, 200


@admin_bp.post("/users/<int:user_id>/make_admin")
@jwt_required()
def make_admin(user_id):
    admin_required()

    user = User.query.get_or_404(user_id)
    user.is_admin = True
    user.approved = True

    db.session.commit()

    return {"message": "User promoted to admin"}, 200


@admin_bp.delete("/users/<int:user_id>")
@jwt_required()
def delete_user(user_id):
    admin_required()

    user = User.query.get_or_404(user_id)

    db.session.delete(user)
    db.session.commit()

    return {"message": "User deleted"}, 200


@admin_bp.patch("/hotels/<int:hotel_id>/approve")
@jwt_required()
def approve_hotel(hotel_id):
    admin_required()

    hotel = Hotel.query.get_or_404(hotel_id)
    hotel.approved = True

    db.session.commit()

    return {"message": "Hotel approved"}, 200


@admin_bp.patch("/hotels/<int:hotel_id>")
@jwt_required()
def admin_edit_hotel(hotel_id):
    admin_required()

    hotel = Hotel.query.get_or_404(hotel_id)
    data = request.get_json() or {}
    hotel.hotel_name = data.get("hotel_name", hotel.hotel_name)
    hotel.address = data.get("address", hotel.address)
    hotel.approved = data.get("approved", hotel.approved)

    db.session.commit()

    return {"message": "Hotel updated successfully"}, 200


@admin_bp.delete("/hotels/<int:hotel_id>")
@jwt_required()
def admin_delete_hotel(hotel_id):
    admin_required()

    hotel = Hotel.query.get_or_404(hotel_id)
    
    db.session.delete(hotel)
    db.session.commit()
    
    return {"message": "Hotel deleted successfully"}, 200