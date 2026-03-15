import uuid
from datetime import datetime

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.ai.receipt_graph import run_receipt_graph
from app.models.item_model import ReceiptItem
from app.models.receipt_model import Receipt
from app.repositories.receipt_repository import ReceiptRepository
from app.repositories.user_repository import UserRepository
from app.services.insight_service import InsightService
from app.services.ocr_service import OCRService
from app.services.storage_service import StorageService
from app.utils.image_utils import guess_content_type


class ReceiptService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repo = ReceiptRepository(db)
        self.user_repo = UserRepository(db)
        self.storage = StorageService()
        self.ocr = OCRService()
        self.insight_service = InsightService(db)

    async def upload_and_process(self, user_id: uuid.UUID, file: UploadFile) -> Receipt:
        self.user_repo.get_or_create(user_id)

        content = await file.read()
        content_type = file.content_type or guess_content_type(file.filename or "receipt.bin")
        image_url = self.storage.upload_receipt(user_id, file.filename or "receipt.bin", content, content_type)

        ocr_result = self.ocr.analyze_receipt_bytes(content)
        graph_state = run_receipt_graph(
            {
                "store_name": ocr_result.get("store_name"),
                "purchase_date": ocr_result.get("purchase_date"),
                "items": ocr_result.get("items", []),
                "total": ocr_result.get("total", 0.0),
            }
        )

        parsed_date = graph_state.get("purchase_date")
        purchase_date = None
        if parsed_date:
            purchase_date = datetime.fromisoformat(parsed_date)

        receipt = Receipt(
            user_id=user_id,
            store_name=graph_state.get("store_name"),
            purchase_date=purchase_date,
            total_amount=float(graph_state.get("total") or 0),
            raw_ocr_json=ocr_result.get("raw"),
            image_url=image_url,
        )

        for item_data in graph_state.get("items", []):
            receipt.items.append(
                ReceiptItem(
                    item_name=item_data.get("item_name", "Unknown"),
                    category=item_data.get("category"),
                    price=float(item_data.get("price") or 0),
                    quantity=int(item_data.get("quantity") or 1),
                    metadata_json={},
                )
            )

        created = self.repo.create(receipt)
        self.insight_service.save_insight(user_id, "spending", graph_state.get("spending_insight", {}))
        self.insight_service.save_insight(user_id, "health", graph_state.get("health_insight", {}))
        return created

    def list_receipts(self, user_id: uuid.UUID) -> list[Receipt]:
        return self.repo.get_all_by_user(user_id)

    def get_receipt(self, receipt_id: uuid.UUID) -> Receipt | None:
        return self.repo.get_by_id(receipt_id)

    def delete_receipt(self, receipt_id: uuid.UUID) -> bool:
        receipt = self.repo.get_by_id(receipt_id)
        if not receipt:
            return False
        self.repo.delete(receipt)
        return True
