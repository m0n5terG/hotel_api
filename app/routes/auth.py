from flask import Blueprint, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from ..extensions import db
from ..models import User

auth_bp = Blueprint("auth", __name__)

@auth_bp.post("/register")
def register_user():
    staff_id = request.form.get("staff_id", "").strip()
    password = request.form.get("password", "").strip()
    name = request.form.get("name", "").strip()
    shortname = request.form.get("shortname", "").strip()
    
    user = User(
        staff_id=staff_id,
        name=name,
        shortname=shortname,
        password_hash=generate_password_hash(password),
        approved=False
    )

    db.session.add(user)
    db.session.commit()

    return {"message": "Registration submitted. Await admin approval."}, 201


@auth_bp.post("/login")
def login():
    data = request.get_json()
    if not data:
        return {"error": "Missing JSON"}, 400

    staff_id = data.get("staff_id", "").strip()
    password = data.get("password", "").strip()
    if not staff_id or not password:
        return {"error": "Missing credentials"}, 400

    user = User.query.filter_by(staff_id=staff_id).first()
    if not user:
        return {"error": "Invalid credentials"}, 401

    if not user.approved:
        return {"error": "User not approved"}, 403

    if not check_password_hash(user.password_hash, password):
        return {"error": "Invalid credentials"}, 401

    token = create_access_token(
        identity=str(user.id),
        additional_claims={"staff_id": user.staff_id, "is_admin": user.is_admin}
    )
    return {"access_token": token}, 200
