from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
import uuid

from app.models import hotel

from ..extensions import db
from ..models import Hotel, HotelPhoto, HotelComment
from ..services.supabase_storage import upload_hotel_photo

hotel_bp = Blueprint("hotel", __name__)


@hotel_bp.get("/hotels")
@jwt_required()
def get_hotels():

    hotels = Hotel.query.filter_by(approved=True).all()

    result = []

    for h in hotels:
        result.append({
            "id": h.id,
            "country_code": h.country_code,
            "hotel_name": h.hotel_name,
            "address": h.address,

            # Thumbnail only
            "thumbnail":
                h.photos[0].image_url if h.photos else None,

            "comment_count":
                HotelComment.query
                .filter_by(hotel_id=h.id)
                .count()
        })

    return result, 200


@hotel_bp.get("/hotels/<int:hotel_id>")
@jwt_required()
def get_hotel_detail(hotel_id):

    h = Hotel.query.get_or_404(hotel_id)

    return {
        "id": h.id,
        "country_code": h.country_code,
        "hotel_name": h.hotel_name,
        "address": h.address,
        "amenities": h.amenities,
        "nearby_amenities": h.nearby_amenities,
        "fb_discount": h.fb_discount,

        "photos": [
            p.image_url for p in h.photos
        ],

        "comments": [
            {
                "comment_id": c.id,
                "crew":
                    c.user.shortname
                    if c.user.shortname
                    else c.user.staff_id,
                "comment": c.comment,
                "created_at": c.created_at
            }
            for c in h.comments
        ]
    }, 200


@hotel_bp.post("/hotels")
@jwt_required()
def create_hotel():

    user_id = int(get_jwt_identity())

    country_code = request.form.get("country_code", "").strip().upper()
    hotel_name = request.form.get("hotel_name", "").strip()
    address = request.form.get("address", "").strip()
    amenities = request.form.get("amenities", "")
    nearby_amenities = request.form.get("nearby_amenities", "")
    fb_discount = request.form.get("fb_discount", "")

    if not country_code or not hotel_name or not address:
        return {"error": "Missing required fields"}, 400

    if Hotel.query.filter_by(
        country_code=country_code,
        hotel_name=hotel_name,
        address=address
    ).first():
        return {"error": "Duplicate hotel"}, 409

    hotel = Hotel(
        country_code=country_code,
        hotel_name=hotel_name,
        address=address,
        amenities=amenities,
        nearby_amenities=nearby_amenities,
        fb_discount=fb_discount,
        approved=False,
        created_by=user_id
    )

    db.session.add(hotel)
    db.session.commit()

    # Upload photos
    files = request.files.getlist("photos")

    if len(files) > 10:
        return {"error": "Maximum 10 photos allowed"}, 400

    for file in files:
        if file.filename == "":
            continue

        image_url = upload_hotel_photo(file)

        db.session.add(
            HotelPhoto(
                hotel_id=hotel.id,
                image_url=image_url
            )
        )

    db.session.commit()

    return {
        "message": "Hotel created successfully",
        "hotel_id": hotel.id
    }, 201


@hotel_bp.post("/hotels/<int:hotel_id>/photos")
@jwt_required()
def add_hotel_photo(hotel_id):

    hotel = Hotel.query.get_or_404(hotel_id)
    photo = request.files.get("photo")

    if not photo:
        return {"error": "Photo required"}, 400

    image_url = upload_hotel_photo(photo)

    db.session.add(
        HotelPhoto(hotel_id=hotel.id, image_url=image_url)
    )
    db.session.commit()

    return {
        "message": "Photo added",
        "image_url": image_url
    }, 201