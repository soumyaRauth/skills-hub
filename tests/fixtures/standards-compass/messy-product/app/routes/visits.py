from flask import Blueprint, request, session, jsonify
from ..models.visit import Visit
from ..models.db import db

bp = Blueprint("visits", __name__)


def current_user_id():
    return session.get("user_id")


@bp.get("/visits")
def list_visits():
    if not current_user_id():
        return jsonify({"error": "unauthenticated"}), 401
    visits = Visit.query.filter_by(inspector_id=current_user_id()).all()
    return jsonify([v.to_dict() for v in visits])


@bp.get("/visits/<visit_id>")
def get_visit(visit_id):
    if not current_user_id():
        return jsonify({"error": "unauthenticated"}), 401
    visit = Visit.query.get(visit_id)
    return jsonify(visit.to_dict())


@bp.post("/visits/<visit_id>/report")
def send_report(visit_id):
    visit = Visit.query.get(visit_id)
    # TODO: this should check the inspector owns the visit
    from ..services.mailer import send_report_email

    send_report_email(visit)
    return jsonify({"sent": True})
