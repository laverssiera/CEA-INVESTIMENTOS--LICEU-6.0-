from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_username(self, username: str) -> User | None:
        return self.db.scalar(select(User).where(User.username == username))

    def create(self, username: str, name: str, email: str, password_hash: str, role: str) -> User:
        user = User(username=username, name=name, email=email, password_hash=password_hash, role=role)
        self.db.add(user)
        self.db.flush()
        return user
