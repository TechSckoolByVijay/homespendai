import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.insight_model import Insight


class InsightRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, insight: Insight) -> Insight:
        self.db.add(insight)
        self.db.commit()
        self.db.refresh(insight)
        return insight

    def get_by_user(self, user_id: uuid.UUID, insight_type: str | None = None) -> list[Insight]:
        stmt = select(Insight).where(Insight.user_id == user_id)
        if insight_type:
            stmt = stmt.where(Insight.insight_type == insight_type)
        stmt = stmt.order_by(Insight.created_at.desc())
        return list(self.db.scalars(stmt).all())
