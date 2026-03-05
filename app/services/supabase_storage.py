import uuid
from supabase import create_client
from flask import current_app


def get_supabase():
    return create_client(
        current_app.config["SUPABASE_URL"],
        current_app.config["SUPABASE_KEY"]
    )


# -----------------------------
# Upload Avatar
# -----------------------------
def upload_avatar(file):

    supabase = get_supabase()

    filename = f"avatar_{uuid.uuid4().hex}.jpg"

    supabase.storage.from_("avatars").upload(
        filename,
        file.read(),
        {"content-type": file.content_type}
    )

    return supabase.storage.from_("avatars").get_public_url(filename)


# ✅ NEW — Upload Hotel Photo
# -----------------------------
def upload_hotel_photo(file):

    supabase = get_supabase()

    filename = f"hotel_{uuid.uuid4().hex}.jpg"

    supabase.storage.from_("hotel-images").upload(
        filename,
        file.read(),
        {"content-type": file.content_type}
    )

    return supabase.storage.from_("hotel-images").get_public_url(filename)