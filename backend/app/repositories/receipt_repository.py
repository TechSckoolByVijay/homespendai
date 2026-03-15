import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.receipt_model import Receipt


class ReceiptRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, receipt: Receipt) -> Receipt:
        self.db.add(receipt)
        self.db.commit()
        self.db.refresh(receipt)
        return receipt

    def get_all_by_user(self, user_id: uuid.UUID) -> list[Receipt]:
        stmt = (
            select(Receipt)
            .where(Receipt.user_id == user_id)
            .options(selectinload(Receipt.items))
            .order_by(Receipt.created_at.desc())
        )
        return list(self.db.scalars(stmt).all())

    def get_by_id(self, receipt_id: uuid.UUID) -> Receipt | None:
        stmt = select(Receipt).where(Receipt.id == receipt_id).options(selectinload(Receipt.items))
        return self.db.scalars(stmt).first()

    def delete(self, receipt: Receipt) -> None:
        self.db.delete(receipt)
        self.db.commit()
