import os
import uuid

from flask import Blueprint, abort, request

bp = Blueprint("uploads", __name__)
ALLOWED = {".png", ".jpg", ".jpeg"}
STORE = os.environ.get("UPLOAD_DIR", "/var/app/uploads")


@bp.post("/photos")
def upload_photo():
    f = request.files.get("photo")
    if f is None:
        abort(400)
    ext = os.path.splitext(f.filename)[1].lower()
    if ext not in ALLOWED:
        abort(415)
    name = f"{uuid.uuid4()}{ext}"
    f.save(os.path.join(STORE, name))
    return {"id": name}, 201
