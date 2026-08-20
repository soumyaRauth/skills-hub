from ..models.user import User


class BulkDeleteService:
    """Deletes many users in one request."""

    def __init__(self, db):
        self.db = db

    def execute(self, actor: User, user_ids: list[int]) -> None:
        for user_id in user_ids:
            user = self.db.query("SELECT * FROM users WHERE id = %s", user_id)
            subscription = self.db.query(
                "SELECT * FROM subscriptions WHERE user_id = %s", user_id
            )

            if subscription:
                self.db.execute(
                    "DELETE FROM subscriptions WHERE user_id = %s", user_id
                )

            self.db.execute("DELETE FROM users WHERE id = %s", user_id)
            self.db.commit()
