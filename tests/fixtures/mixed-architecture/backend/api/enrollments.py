from fastapi import APIRouter, Depends

from ..models.enrollment import Enrollment
from ..services.enrollment_service import EnrollmentService

router = APIRouter(prefix="/enrollments")


def serialize(enrollment: Enrollment) -> dict:
    return {
        "id": enrollment.id,
        "course_id": enrollment.course_id,
        "status": enrollment.status.value,
        "completed_at": (
            enrollment.completed_at.isoformat() if enrollment.completed_at else None
        ),
    }


@router.post("/{enrollment_id}/complete")
def complete(enrollment_id: int, service: EnrollmentService = Depends()) -> dict:
    enrollment = service.repository.get(enrollment_id)
    return serialize(service.complete_enrollment(enrollment))
