import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.insight_schema import (
    CategoryBreakdownResponse,
    HealthInsightsResponse,
    MonthlyInsightsResponse,
)
from app.services.insight_service import InsightService


router = APIRouter(prefix="/insights", tags=["insights"])


@router.get("/monthly", response_model=MonthlyInsightsResponse)
def get_monthly_insights(user_id: uuid.UUID, db: Session = Depends(get_db)) -> MonthlyInsightsResponse:
    service = InsightService(db)
    insights = service.get_insights(user_id, insight_type="spending")
    highlights = [f"{entry.insight_data.get('top_category', 'other')} dominated your spending" for entry in insights[:3]]
    return MonthlyInsightsResponse(month="current", highlights=highlights)


@router.get("/health", response_model=HealthInsightsResponse)
def get_health_insights(user_id: uuid.UUID, db: Session = Depends(get_db)) -> HealthInsightsResponse:
    service = InsightService(db)
    insights = service.get_insights(user_id, insight_type="health")
    if not insights:
        return HealthInsightsResponse(score=0, notes=["No health insights yet"])
    latest = insights[0].insight_data
    return HealthInsightsResponse(score=int(latest.get("health_score", 0)), notes=latest.get("notes", []))


@router.get("/category-breakdown", response_model=CategoryBreakdownResponse)
def get_category_breakdown(user_id: uuid.UUID, db: Session = Depends(get_db)) -> CategoryBreakdownResponse:
    service = InsightService(db)
    insights = service.get_insights(user_id, insight_type="spending")
    categories: dict[str, float] = {}
    for insight in insights:
        breakdown = insight.insight_data.get("category_breakdown", {})
        for category, amount in breakdown.items():
            categories[category] = categories.get(category, 0.0) + float(amount or 0)
    return CategoryBreakdownResponse(categories=categories)
