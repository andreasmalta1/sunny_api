from fastapi import status, HTTPException, Depends, APIRouter, Request
from sqlalchemy.orm import Session

try:
    from app.database import get_db
    from app.utils import post_request
    import app.schemas as schemas
    import app.models as models
    import app.utils as utils
except ImportError:
    from database import get_db
    from utils import post_request
    import schemas
    import models
    import utils

router = APIRouter(prefix="/api/users", tags=["Users"])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.UserResponse,
    include_in_schema=False,
)
def create_user(
    request: Request, user: schemas.UserCreate, db: Session = Depends(get_db)
):
    user.password = utils.hash(user.password)

    results = db.query(models.User).all()
    if len(results) != 0:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Cannot create user",
        )

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    post_request(db, "users", request)

    return new_user
