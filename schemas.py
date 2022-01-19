from typing import Optional
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    uuid: str


class UserBase(BaseModel):
    email: str
    role: str
    last_scrip_id: int


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None


class User(UserBase):
    uuid: str

    class Config:
        orm_mode = True


class ItemCreate(BaseModel):
    content: str


class Script(BaseModel):
    content: str

    class Config:
        orm_mode = True


class Scripts(Script):
    script_id: int

    class Config:
        orm_mode = True


class ScriptDB(Scripts):
    uuid: str

    class Config:
        orm_mode = True
