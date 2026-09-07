import os
import uuid
from flask import Blueprint, request, session, jsonify, send_file

bp = Blueprint("uploads", __name__)
UPLOAD_DIR = os.environ.get("UPLOAD_DIR", "/var/data/uploads")


@bp.post("/uploads")
def upload():
    if not session.get("user_id"):
        return jsonify({"error": "unauthenticated"}), 401
    f = request.files["photo"]
    name = f"{uuid.uuid4()}-{f.filename}"
    f.save(os.path.join(UPLOAD_DIR, name))
    return jsonify({"name": name})


@bp.get("/uploads/<name>")
def fetch(name):
    return send_file(os.path.join(UPLOAD_DIR, name))
