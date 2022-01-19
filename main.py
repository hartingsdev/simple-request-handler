from datetime import timedelta

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import models
import schemas
from security import authenticate_user, create_access_token
from settings import ACCESS_TOKEN_EXPIRE_MINUTES
from database import get_db, engine
from user import router as user_router
from items import router as item_router
from script import router as script_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(user_router)
app.include_router(item_router)
app.include_router(script_router)


@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username,
                             form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"uuid": user.uuid}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
