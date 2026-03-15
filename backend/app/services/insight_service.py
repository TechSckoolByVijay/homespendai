import uuid

from sqlalchemy.orm import Session

from app.models.insight_model import Insight
from app.repositories.insight_repository import InsightRepository


class InsightService:
    def __init__(self, db: Session) -> None:
        self.repo = InsightRepository(db)

    def save_insight(self, user_id: uuid.UUID, insight_type: str, insight_data: dict) -> Insight:
        insight = Insight(user_id=user_id, insight_type=insight_type, insight_data=insight_data)
        return self.repo.create(insight)

    def get_insights(self, user_id: uuid.UUID, insight_type: str | None = None) -> list[Insight]:
        return self.repo.get_by_user(user_id, insight_type=insight_type)
