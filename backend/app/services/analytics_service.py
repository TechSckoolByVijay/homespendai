import uuid

from sqlalchemy.orm import Session

from app.repositories.receipt_repository import ReceiptRepository


class AnalyticsService:
    def __init__(self, db: Session) -> None:
        self.repo = ReceiptRepository(db)

    def spending_trend(self, user_id: uuid.UUID) -> list[dict]:
        receipts = self.repo.get_all_by_user(user_id)
        monthly: dict[str, float] = {}
        for receipt in receipts:
            month = receipt.created_at.strftime("%Y-%m")
            monthly[month] = monthly.get(month, 0.0) + float(receipt.total_amount or 0)

        return [{"period": key, "amount": round(value, 2)} for key, value in sorted(monthly.items())]

    def store_frequency(self, user_id: uuid.UUID) -> dict[str, int]:
        receipts = self.repo.get_all_by_user(user_id)
        counts: dict[str, int] = {}
        for receipt in receipts:
            store = receipt.store_name or "Unknown"
            counts[store] = counts.get(store, 0) + 1
        return counts
