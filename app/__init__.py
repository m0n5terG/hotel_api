from flask import Flask
from .config import Config
from .extensions import db, jwt

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)

    # ✅ IMPORT MODELS FIRST
    from .models import User, Hotel, HotelComment, HotelPhoto

    # ✅ THEN CREATE TABLES
    with app.app_context():
        db.create_all()

    # Register blueprints
    from .routes.auth import auth_bp
    from .routes.profile import profile_bp
    from .routes.hotels import hotel_bp
    from .routes.comment import comment_bp
    from .routes.admin import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(hotel_bp)
    app.register_blueprint(comment_bp)
    app.register_blueprint(admin_bp)

    return app