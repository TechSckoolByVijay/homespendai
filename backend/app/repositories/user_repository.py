import uuid

from sqlalchemy import delete, select, update
from sqlalchemy.orm import Session

from app.models.insight_model import Insight, SpendingSummary
from app.models.receipt_model import Receipt
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

    def migrate_user_data(self, source_user_id: uuid.UUID, target_user_id: uuid.UUID) -> None:
        if source_user_id == target_user_id:
            return

        self.db.execute(
            update(Receipt)
            .where(Receipt.user_id == source_user_id)
            .values(user_id=target_user_id)
        )
        self.db.execute(
            update(Insight)
            .where(Insight.user_id == source_user_id)
            .values(user_id=target_user_id)
        )
        self.db.execute(
            update(SpendingSummary)
            .where(SpendingSummary.user_id == source_user_id)
            .values(user_id=target_user_id)
        )
        self.db.execute(delete(User).where(User.id == source_user_id))
        self.db.commit()

    def register_with_email(self, email: str, current_user_id: uuid.UUID | None = None) -> User:
        email_user = self.get_by_email(email)
        current_user = self.get_by_id(current_user_id) if current_user_id else None

        if email_user and current_user and email_user.id != current_user.id:
            self.migrate_user_data(current_user.id, email_user.id)
            self.db.refresh(email_user)
            return email_user

        if email_user:
            return email_user

        if current_user:
            current_user.email = email
            self.db.commit()
            self.db.refresh(current_user)
            return current_user

        return self.get_or_create_by_email(email)

    def get_or_create(self, user_id: uuid.UUID, email: str | None = None) -> User:
        user = self.get_by_id(user_id)
        if user:
            return user
        user = User(id=user_id, email=email or f"user-{str(user_id)[:8]}@local.dev")
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
