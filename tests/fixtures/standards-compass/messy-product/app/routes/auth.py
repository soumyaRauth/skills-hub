import hashlib
from flask import Blueprint, request, session, jsonify
from ..models.user import User

bp = Blueprint("auth", __name__)


@bp.post("/login")
def login():
    user = User.query.filter_by(email=request.form["email"]).first()
    if not user:
        return jsonify({"error": "unknown email"}), 404
    digest = hashlib.sha256(request.form["password"].encode()).hexdigest()
    if digest != user.password_hash:
        return jsonify({"error": "wrong password"}), 401
    session["user_id"] = user.id
    return jsonify({"ok": True})


@bp.post("/logout")
def logout():
    session.pop("user_id", None)
    return jsonify({"ok": True})
