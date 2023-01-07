from fastapi import status, APIRouter, HTTPException, Response, Depends, Request
from sqlalchemy.orm import Session
from typing import List, Optional
import random

try:
    from app.database import get_db
    import app.schemas as schemas
    import app.models as models
    import app.oauth2 as oauth2
except ImportError:
    from database import get_db
    import schemas
    import models
    import oauth2


router = APIRouter(prefix="/api/quotes", tags=["Quotes"])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.QuoteResponse,
    include_in_schema=False,
)
def create_quote(
    quote: schemas.QuoteCreate,
    current_user: int = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db),
):

    if current_user.id != 1:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Unauthorized action",
        )

    new_quote = models.Quote(**quote.dict())
    db.add(new_quote)
    db.commit()
    db.refresh(new_quote)

    return new_quote


@router.get("/", response_model=List[schemas.QuoteResponse])
def get_quotes(
    db: Session = Depends(get_db),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
):

    results = (
        db.query(models.Quote)
        .filter(models.Quote.quote.contains(search))
        .order_by(models.Quote.id)
        .limit(limit)
        .offset(skip)
        .all()
    )

    return results
