from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class EnrollmentStatus(str, Enum):
    ENROLLED = "enrolled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    WITHDRAWN = "withdrawn"


@dataclass
class Enrollment:
    id: int
    user_id: int
    course_id: int
    status: EnrollmentStatus
    completed_at: datetime | None = None
