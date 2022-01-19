from sqlalchemy.exc import IntegrityError
import random
import string
from database import SessionLocal
from crud import create_user
from schemas import UserCreate


def create_user_account():
    password = "".join(random.choice(string.ascii_letters) for _ in range(10))
    user = UserCreate(
        email="admin@localhost",
        role="admin",
        last_scrip_id=0,
        password=password
    )
    db = SessionLocal()
    try:
        create_user(db, user)
    except IntegrityError:
        print(f"User {user.email} already exists.")
    else:
        print(f"User with email {user.email} was created "
              f"with password {user.password}")


if __name__ == "__main__":
    create_user_account()
