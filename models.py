from sqlalchemy import Boolean, Column, String, CHAR, Integer, ForeignKey

from database import Base


class User(Base):
    __tablename__ = "users"

    uuid = Column(CHAR(32), primary_key=True, index=True, autoincrement=False)
    email = Column(String, unique=True, index=True)
    role = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    last_scrip_id = Column(Integer, default=0)


class Script(Base):
    __tablename__ = "scripts"

    script_id = Column(Integer, primary_key=True)
    uuid = Column(CHAR(32), ForeignKey('users.uuid', ondelete='CASCADE'),
                  primary_key=True, index=True, autoincrement=False)
    content = Column(String)
