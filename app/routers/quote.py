from fastapi import status, APIRouter, HTTPException, Response, Depends, Request
from sqlalchemy.orm import Session
from typing import List, Optional
import random

try:
    from app.database import get_db
    from app.utils import post_request, get_team_return
    import app.schemas as schemas
    import app.models as models
    import app.oauth2 as oauth2
except ImportError:
    from database import get_db
    from utils import post_request, get_team_return
    import schemas
    import models
    import oauth2


router = APIRouter(prefix="/api/teams", tags=["Teams"])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.TeamResponse,
    include_in_schema=False,
)
def create_team(
    request: Request,
    team: schemas.TeamCreate,
    current_user: int = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db),
):

    if current_user.id != 1:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Unauthorized action",
        )

    new_team = models.Team(**team.dict())
    db.add(new_team)
    db.commit()
    db.refresh(new_team)

    post_request(db, "teams", request)

    return new_team


@router.get("/", response_model=List[schemas.TeamResponse])
def get_teams(
    request: Request,
    db: Session = Depends(get_db),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
):

    results = (
        db.query(models.Team)
        .filter(models.Team.full_name.contains(search))
        .order_by(models.Team.id)
        .limit(limit)
        .offset(skip)
        .all()
    )

    return_results = [get_team_return(team) for team in results]

    post_request(db, "teams", request)

    return return_results


@router.get("/random", response_model=schemas.TeamResponse)
def get_random_team(request: Request, db: Session = Depends(get_db)):

    results = db.query(models.Team).all()
    if not results:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No teams found",
        )
    team = random.choice(results)
    team_return = get_team_return(team)

    post_request(db, "teams", request)

    return team_return


@router.get("/{id}", response_model=schemas.TeamResponse)
def get_team(id: int, request: Request, db: Session = Depends(get_db)):
    team = db.query(models.Team).filter(models.Team.id == id).first()

    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team with id {id} was not found",
        )

    team_return = get_team_return(team)
    post_request(db, "teams", request)

    return team_return


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, include_in_schema=False)
def delete_team(
    request: Request,
    id: int,
    current_user: int = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db),
):

    if current_user.id != 1:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Unauthorized action",
        )

    team_query = db.query(models.Team).filter(models.Team.id == id)
    team = team_query.first()

    if team == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team with id {id} was not found",
        )

    team_query.delete(synchronize_session=False)
    db.commit()

    post_request(db, "teams", request)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.TeamResponse, include_in_schema=False)
def update_team(
    request: Request,
    id: int,
    updated_team: schemas.TeamCreate,
    current_user: int = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db),
):

    if current_user.id != 1:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Unauthorized action",
        )

    team_query = db.query(models.Team).filter(models.Team.id == id)
    team = team_query.first()

    if team == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team with id {id} was not found",
        )

    team_query.update(updated_team.dict(), synchronize_session=False)
    db.commit()

    post_request(db, "teams", request)

    return team_query.first()
