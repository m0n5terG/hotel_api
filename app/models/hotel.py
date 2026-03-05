from datetime import datetime
from ..extensions import db

class Hotel(db.Model):
    __tablename__ = "hotels"

    id = db.Column(db.Integer, primary_key=True)
    country_code = db.Column(db.String(3), nullable=False)
    hotel_name = db.Column(db.String(150), nullable=False)
    address = db.Column(db.String(250), nullable=False)
    amenities = db.Column(db.Text)
    nearby_amenities = db.Column(db.Text)
    fb_discount = db.Column(db.String(100))
    approved = db.Column(db.Boolean, default=False)
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    photos = db.relationship("HotelPhoto", backref="hotel", cascade="all, delete", lazy=True)
    comments = db.relationship("HotelComment", backref="hotel", cascade="all, delete", lazy=True)

    __table_args__ = (
        db.UniqueConstraint("country_code", "hotel_name", "address", name="unique_hotel_constraint"),
    )