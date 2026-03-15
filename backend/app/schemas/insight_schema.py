import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class InsightResponse(BaseModel):
    id: uuid.UUID
    insight_type: str
    insight_data: dict = Field(default_factory=dict)
    created_at: datetime


class MonthlyInsightsResponse(BaseModel):
    month: str
    highlights: list[str] = Field(default_factory=list)


class HealthInsightsResponse(BaseModel):
    score: int
    notes: list[str] = Field(default_factory=list)


class CategoryBreakdownResponse(BaseModel):
    categories: dict[str, float] = Field(default_factory=dict)
