from datetime import timedelta

class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///../instance/test.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = "change-this-secret"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=12)

    SUPABASE_URL = "url"
    SUPABASE_KEY = "secret key"