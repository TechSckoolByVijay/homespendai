from pydantic import BaseModel, Field


class SpendingTrendPoint(BaseModel):
    period: str
    amount: float


class SpendingTrendResponse(BaseModel):
    points: list[SpendingTrendPoint] = Field(default_factory=list)


class StoreFrequencyResponse(BaseModel):
    stores: dict[str, int] = Field(default_factory=dict)
