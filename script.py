from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Response
import schemas
import crud
from security import get_current_active_user
from database import get_db

router = APIRouter(prefix="/s", tags=["script"])


@router.get("/", response_model=list[schemas.Scripts])
def get_all_scripts_of_user(skip: int = 0, limit: int = 100,
                            current_user: schemas.User =
                            Depends(get_current_active_user),
                            db: Session = Depends(get_db)):
    return crud.get_all_scripts_of_user(db, current_user.uuid, skip, limit)


@router.post("/")  # , status_code=204)
def create_script(script: schemas.Script,
                  current_user: schemas.User = Depends(get_current_active_user),
                  db: Session = Depends(get_db)):
    return crud.create_script(db, current_user, script)
    # return Response(status_code=204)


@router.delete("/", status_code=204)
def del_all_scripts_of_user(current_user: schemas.User =
                            Depends(get_current_active_user),
                            db: Session = Depends(get_db)):
    crud.delete_all_scripts_of_user(db, current_user.uuid)
    return Response(status_code=204)


@router.delete("/{script_id}", status_code=204)
def del_a_script_of_user(script_id: int,
                         current_user: schemas.User = Depends(
                             get_current_active_user),
                         db: Session = Depends(get_db)):
    crud.delete_a_script_of_user(db, current_user.uuid, script_id)
    return Response(status_code=204)


@router.get("/{script_id}/{uuid}")
def get_a_script_of_user(script_id: int, uuid: str,
                         db: Session = Depends(get_db)):
    script = crud.get_a_script_of_user(db, uuid, script_id)
    return Response(content=script.content, media_type="text/javascript")
