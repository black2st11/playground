from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=list[schemas.User])
def get_users(
    db: Session = Depends(deps.get_db),
    offset: int = 0,
    limit: int = 100,
    current_user: models.user.User = Depends(deps.get_current_active_superuser),
) -> Any:
    users = crud.user.get_multi(db=db, offset=offset, limit=limit)
    return users


@router.post("/", response_model=schemas.User)
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserCreate,
    current_user: models.user.User = Depends(deps.get_current_active_superuser)
):
    user = crud.user.get_by_email(db=db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400, detail="existed username, please submit another username"
        )
    user = crud.user.create(db=db, obj_in=user_in)
    return user


@router.get("/me", response_model=schemas.User)
def get_me(
    db: Session = Depends(deps.get_db),
    current_user: models.user.User = Depends(deps.get_current_active_user),
):
    return current_user


@router.put("/me", response_model=schemas.User)
def update_me(
    db: Session = Depends(deps.get_db),
    password: str = Body(None),
    name: str = Body(None),
    email: str = Body(None),
    current_user: models.user.User = Depends(deps.get_current_active_user),
):
    current_user_data = jsonable_encoder(**current_user)
    user_in = schemas.UserUpdate(**current_user_data)
    if password:
        user_in.password = password
    if name:
        user_in.name = name
    if email:
        user_in.email = email

    user = crud.user.update(db=db, db_obj=current_user, obj_in=user_in)
    return user
