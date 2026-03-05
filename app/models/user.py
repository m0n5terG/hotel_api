from datetime import datetime
from ..extensions import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    staff_id = db.Column(db.String(8), unique=True, nullable=False)
    name = db.Column(db.String(100))  # Full name
    shortname = db.Column(db.String(50))  # Crew nickname / AKA
    password_hash = db.Column(db.String(255), nullable=False)
    photo = db.Column(db.String(255), nullable=True)
    approved = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)