from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends, APIRouter

import crud
import schemas

from security import get_current_active_user
from database import get_db

router = APIRouter(prefix="/users", tags=["user"])


@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate,
                current_user: schemas.User = Depends(get_current_active_user),
                db: Session = Depends(get_db)):
    if current_user.role != "admin":
        raise HTTPException(status_code=401, detail="No permission")
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@router.get("/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100,
               current_user: schemas.User = Depends(get_current_active_user),
               db: Session = Depends(get_db)):
    if current_user.role != "admin":
        raise HTTPException(status_code=401, detail="No permission")
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/me/", response_model=schemas.User)
async def read_users_me(current_user: schemas.User =
                        Depends(get_current_active_user)):
    return current_user


@router.get("/{uuid}", response_model=schemas.User)
def read_user(uuid: str,
              current_user: schemas.User = Depends(get_current_active_user),
              db: Session = Depends(get_db)):
    if current_user.role != "admin":
        raise HTTPException(status_code=401, detail="No permission")
    db_user = crud.get_user(db, uuid=uuid)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.put("/{uuid}", response_model=schemas.User)
def update_user(uuid: str,
                new_info: schemas.UserUpdate,
                current_user: schemas.User = Depends(get_current_active_user),
                db: Session = Depends(get_db)):
    if uuid != current_user.uuid and current_user.role != "admin":
        raise HTTPException(status_code=401, detail="No permission")
    db_user = crud.get_user(db, uuid=uuid)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_user = crud.update_user(db, db_user, new_info)
    return db_user
