import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.analytics_schema import StoreFrequencyResponse, SpendingTrendResponse
from app.services.analytics_service import AnalyticsService


router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/spending-trend", response_model=SpendingTrendResponse)
def spending_trend(user_id: uuid.UUID, db: Session = Depends(get_db)) -> SpendingTrendResponse:
    service = AnalyticsService(db)
    return SpendingTrendResponse(points=service.spending_trend(user_id))


@router.get("/store-frequency", response_model=StoreFrequencyResponse)
def store_frequency(user_id: uuid.UUID, db: Session = Depends(get_db)) -> StoreFrequencyResponse:
    service = AnalyticsService(db)
    return StoreFrequencyResponse(stores=service.store_frequency(user_id))
