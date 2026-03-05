from ..extensions import db

class HotelPhoto(db.Model):
    __tablename__ = "hotel_photos"

    id = db.Column(db.Integer, primary_key=True)
    hotel_id = db.Column(db.Integer, db.ForeignKey("hotels.id"), nullable=False)
    image_url = db.Column(db.String(500), nullable=False)
