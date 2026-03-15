import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class ReceiptItem(BaseModel):
    item_name: str
    category: str | None = None
    price: float | None = None
    quantity: int | None = None


class ReceiptUpload(BaseModel):
    user_id: uuid.UUID


class ReceiptResponse(BaseModel):
    id: uuid.UUID
    store_name: str | None
    purchase_date: datetime | None
    total_amount: float | None
    image_url: str
    items: list[ReceiptItem] = Field(default_factory=list)


class ReceiptDeleteResponse(BaseModel):
    message: str
