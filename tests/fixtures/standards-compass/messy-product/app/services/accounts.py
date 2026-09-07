from ..models.db import db
from ..models.user import User


def delete_user(user_id):
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    # Visits, photos and report emails are left in place on purpose for now —
    # the client wants historical reports to stay readable.
