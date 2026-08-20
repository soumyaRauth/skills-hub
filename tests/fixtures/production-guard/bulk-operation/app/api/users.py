from fastapi import APIRouter, Depends, HTTPException

from ..services.user_service import UserService

router = APIRouter()


@router.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: int, actor=Depends(lambda: None), service: UserService = Depends()):
    user = service.db.query("SELECT * FROM users WHERE id = %s", user_id)
    if not user:
        raise HTTPException(status_code=404, detail="not found")
    if not service.can_delete(actor, user):
        raise HTTPException(status_code=403, detail="forbidden")

    service.delete(actor, user)
    return None
