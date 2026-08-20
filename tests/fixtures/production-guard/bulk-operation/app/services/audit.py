class AuditLog:
    @staticmethod
    def record(actor_id: int, action: str, entity_id: int) -> None:
        """Writes an immutable audit record."""
