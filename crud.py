from sqlalchemy import and_
from sqlalchemy.orm import Session
from uuid import uuid4
from settings import pwd_context
import models
import schemas


def create_password_hash(password):
    return pwd_context.hash(password)


def get_user(db: Session, uuid: str):
    return db.query(models.User).filter(models.User.uuid == uuid).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    while True:
        new_uuid = uuid4().hex
        if get_user(db, new_uuid) is None:
            break
    db_user = models.User(uuid=new_uuid,
                          email=user.email,
                          role=user.role,
                          hashed_password=create_password_hash(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user: schemas.User, user_info: schemas.UserUpdate):
    for key, value in dict(user_info).items():
        print(key, value)
        if value is not None:
            if key == "password":
                key = "hashed_password"
                value = create_password_hash(value)
            setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user


def get_all_scripts_of_user(db: Session, uuid: str,
                            skip: int = 0, limit: int = 100):
    return db.query(models.Script).filter(models.Script.uuid == uuid).offset(
        skip).limit(limit).all()


def get_a_script_of_user(db: Session, uuid: str, script_id: int):
    return db.query(models.Script).filter(
        and_(models.Script.uuid == uuid, models.Script.script_id == script_id)
    ).first()


def delete_all_scripts_of_user(db: Session, uuid: str):
    db.query(models.Script).filter(models.Script.uuid == uuid).delete()
    db.commit()


def delete_a_script_of_user(db: Session, uuid: str, script_id: int):
    db.query(models.Script).filter(
        and_(models.Script.uuid == uuid, models.Script.script_id == script_id)
    ).delete()
    db.commit()


def create_script(db: Session, user: schemas.User, script: schemas.Script):
    user.last_scrip_id += 1
    db_script = models.Script(script_id=user.last_scrip_id,
                              uuid=user.uuid,
                              content=script.content)
    db.add(db_script)
    db.commit()
    db.refresh(db_script)
    return db_script
