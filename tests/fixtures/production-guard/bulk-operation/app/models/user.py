from dataclasses import dataclass


@dataclass
class User:
    id: int
    email: str
    team_id: int
    deleted_at: str | None = None
