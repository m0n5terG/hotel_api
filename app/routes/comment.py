from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..extensions import db
from ..models import User, Hotel, HotelComment

comment_bp = Blueprint("comment", __name__)


@comment_bp.post("/hotels/<int:hotel_id>/comments")
@jwt_required()
def add_comment(hotel_id):
    hotel = Hotel.query.get_or_404(hotel_id)
    data = request.get_json()
    if not data or not data.get("comment"):
        return {"error": "Comment required"}, 400

    user = User.query.get(int(get_jwt_identity()))
    comment = HotelComment(hotel_id=hotel.id, user_id=user.id, comment=data["comment"])
    db.session.add(comment)
    db.session.commit()

    return {
        "message": "Comment added",
        "comment_id": comment.id,
        "staff_id": user.staff_id,
        "crew_name": getattr(user, "name", ""),  # optional if name field exists
        "comment": comment.comment,
        "created_at": comment.created_at
    }, 201


@comment_bp.get("/hotels/<int:hotel_id>/comments")
@jwt_required()
def get_comments(hotel_id):
    Hotel.query.get_or_404(hotel_id)
    comments = HotelComment.query.filter_by(hotel_id=hotel_id).order_by(HotelComment.created_at.desc()).all()
    return [
        {
            "comment_id": c.id,
            "staff_id": c.user.staff_id,
            "crew_name": getattr(c.user, "name", ""),
            "comment": c.comment,
            "created_at": c.created_at
        } for c in comments
    ], 200


@comment_bp.put("/comments/<int:comment_id>")
@jwt_required()
def edit_comment(comment_id):
    comment = HotelComment.query.get_or_404(comment_id)
    user = User.query.get(int(get_jwt_identity()))
    if comment.user_id != user.id and not user.is_admin:
        return {"error": "Not authorized"}, 403
    data = request.get_json()
    if not data.get("comment"):
        return {"error": "Comment required"}, 400
    comment.comment = data["comment"]
    db.session.commit()
    return {"message": "Comment updated", "comment": comment.comment}, 200


@comment_bp.delete("/comments/<int:comment_id>")
@jwt_required()
def delete_comment(comment_id):
    comment = HotelComment.query.get_or_404(comment_id)
    user = User.query.get(int(get_jwt_identity()))
    if comment.user_id != user.id and not user.is_admin:
        return {"error": "Not authorized"}, 403
    db.session.delete(comment)
    db.session.commit()
    return {"message": "Comment deleted"}, 200
