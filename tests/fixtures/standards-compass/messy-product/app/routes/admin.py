from flask import Blueprint, session, jsonify
from ..models.user import User
from ..models.visit import Visit

bp = Blueprint("admin", __name__, url_prefix="/admin")


def is_admin():
    uid = session.get("user_id")
    if not uid:
        return False
    user = User.query.get(uid)
    return user.role == "admin"


@bp.get("/users")
def users():
    if not is_admin():
        return jsonify({"error": "forbidden"}), 403
    return jsonify([u.to_dict() for u in User.query.all()])


@bp.get("/visits")
def all_visits():
    if not is_admin():
        return jsonify({"error": "forbidden"}), 403
    return jsonify([v.to_dict() for v in Visit.query.all()])


@bp.post("/users/<user_id>/delete")
def delete_user(user_id):
    if not is_admin():
        return jsonify({"error": "forbidden"}), 403
    from ..services.accounts import delete_user as do_delete

    do_delete(user_id)
    return jsonify({"deleted": True})
