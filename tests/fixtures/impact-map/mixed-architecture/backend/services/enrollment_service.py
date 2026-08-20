from datetime import datetime, timezone

from ..models.enrollment import Enrollment, EnrollmentStatus


class EnrollmentService:
    """Owns every legitimate transition of Enrollment.status."""

    def __init__(self, repository):
        self.repository = repository

    def complete_enrollment(self, enrollment: Enrollment) -> Enrollment:
        if enrollment.status is EnrollmentStatus.COMPLETED:
            return enrollment

        enrollment.status = EnrollmentStatus.COMPLETED
        enrollment.completed_at = datetime.now(timezone.utc)
        self.repository.save(enrollment)
        return enrollment

    def withdraw(self, enrollment: Enrollment) -> Enrollment:
        enrollment.status = EnrollmentStatus.WITHDRAWN
        self.repository.save(enrollment)
        return enrollment
