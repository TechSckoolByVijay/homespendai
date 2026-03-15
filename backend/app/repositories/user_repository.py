import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user_model import User


class UserRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, user_id: uuid.UUID) -> User | None:
        stmt = select(User).where(User.id == user_id)
        return self.db.scalars(stmt).first()

    def get_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        return self.db.scalars(stmt).first()

    def get_or_create_by_email(self, email: str) -> User:
        user = self.get_by_email(email)
        if user:
            return user
        user = User(email=email)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_or_create(self, user_id: uuid.UUID, email: str | None = None) -> User:
        user = self.get_by_id(user_id)
        if user:
            return user
        user = User(id=user_id, email=email or f"user-{str(user_id)[:8]}@local.dev")
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
