from fastapi import APIRouter, Depends, HTTPException

from ..services.bulk_delete import BulkDeleteService

router = APIRouter()


@router.post("/users/bulk-delete", status_code=204)
def bulk_delete(
    payload: dict,
    actor=Depends(lambda: None),
    service: BulkDeleteService = Depends(),
):
    if not actor or not actor.is_admin:
        raise HTTPException(status_code=403, detail="forbidden")

    service.execute(actor, payload["user_ids"])
    return None
