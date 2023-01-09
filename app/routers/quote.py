from fastapi import status, APIRouter, HTTPException, Response, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import List
from pydantic import create_model
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

query_params_strings = {"quote": (str, None), "character": (str, None)}
query_params_integers = {
    "season": (int, 0),
    "episode": (int, 0),
}

query_model_strings = create_model("Query", **query_params_strings)
query_model_integers = create_model("Query", **query_params_integers)


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
    param_strings: query_model_strings = Depends(),
    param_integers: query_model_integers = Depends(),
):

    param_strings_dict = param_strings.dict()
    param_integers_dict = param_integers.dict()
    results = db.query(models.Quote)

    for key in param_strings_dict:
        if param_strings_dict[key]:
            results = results.filter(
                func.lower(getattr(models.Quote, key)).contains(
                    param_strings_dict[key].lower()
                )
            )

    for key in param_integers_dict:
        if param_integers_dict[key]:
            results = results.filter(
                getattr(models.Quote, key) == param_integers_dict[key]
            )

    results = results.order_by(models.Quote.id).limit(limit).offset(skip).all()

    return results


@router.get("/random", response_model=schemas.QuoteResponse)
def get_random_quote(
    db: Session = Depends(get_db),
    param_strings: query_model_strings = Depends(),
    param_integers: query_model_integers = Depends(),
):

    param_strings_dict = param_strings.dict()
    param_integers_dict = param_integers.dict()
    results = db.query(models.Quote)

    for key in param_strings_dict:
        if param_strings_dict[key]:
            results = results.filter(
                func.lower(getattr(models.Quote, key)).contains(
                    param_strings_dict[key].lower()
                )
            )

    for key in param_integers_dict:
        if param_integers_dict[key]:
            results = results.filter(
                getattr(models.Quote, key) == param_integers_dict[key]
            )

    results = results.all()

    if not results:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No quotes found",
        )

    quote = random.choice(results)

    return quote


@router.get("/{id}", response_model=schemas.QuoteResponse)
def get_quotes(id: int, db: Session = Depends(get_db)):
    quote = db.query(models.Quote).filter(models.Quote.id == id).first()

    if not quote:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Quote with id {id} was not found",
        )

    return quote


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, include_in_schema=False)
def delete_quote(
    id: int,
    current_user: int = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db),
):

    if current_user.id != 1:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Unauthorized action",
        )

    quote_query = db.query(models.Quote).filter(models.Quote.id == id)
    quote = quote_query.first()

    if quote == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Quote with id {id} was not found",
        )

    quote_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.QuoteResponse, include_in_schema=False)
def update_quote(
    id: int,
    updated_quote: schemas.QuoteCreate,
    current_user: int = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db),
):

    if current_user.id != 1:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Unauthorized action",
        )

    quote_query = db.query(models.Quote).filter(models.Quote.id == id)
    quote = quote_query.first()

    if quote == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Quote with id {id} was not found",
        )

    quote_query.update(updated_quote.dict(), synchronize_session=False)
    db.commit()

    return quote_query.first()
