from ..models.user import User
from .audit import AuditLog


class UserService:
    """Single-user operations. Note the audit call — the bulk path omits it."""

    def __init__(self, db):
        self.db = db

    def delete(self, actor: User, user: User) -> None:
        if not self.can_delete(actor, user):
            raise PermissionError("not allowed")

        subscription = self.db.query(
            "SELECT * FROM subscriptions WHERE user_id = %s", user.id
        )
        if subscription:
            self.db.execute("DELETE FROM subscriptions WHERE user_id = %s", user.id)

        self.db.execute("DELETE FROM users WHERE id = %s", user.id)
        AuditLog.record(actor_id=actor.id, action="user.deleted", entity_id=user.id)

    def can_delete(self, actor: User, user: User) -> bool:
        return actor.team_id == user.team_id
