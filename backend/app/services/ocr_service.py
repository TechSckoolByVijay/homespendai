from datetime import datetime
import importlib
from typing import Any

from app.config import settings


class OCRService:
    def __init__(self) -> None:
        self.client = None
        if settings.azure_docintel_endpoint and settings.azure_docintel_key:
            ai_docintel = importlib.import_module("azure.ai.documentintelligence")
            azure_core = importlib.import_module("azure.core.credentials")
            self.client = ai_docintel.DocumentIntelligenceClient(
                endpoint=settings.azure_docintel_endpoint,
                credential=azure_core.AzureKeyCredential(settings.azure_docintel_key),
            )

    def analyze_receipt_bytes(self, content: bytes) -> dict:
        if self.client is None:
            return {
                "store_name": "Unknown Store",
                "purchase_date": datetime.utcnow().isoformat(),
                "items": [],
                "total": 0.0,
                "raw": {"warning": "Azure Document Intelligence not configured."},
            }

        poller = self.client.begin_analyze_document("prebuilt-receipt", body=content)
        result: Any = poller.result()
        document = result.documents[0] if result.documents else None
        fields = document.fields if document else {}

        items = []
        item_field = fields.get("Items") if fields else None
        if item_field and item_field.value_array:
            for entry in item_field.value_array:
                value_obj = entry.value_object or {}
                desc = value_obj.get("Description")
                price = value_obj.get("TotalPrice")
                quantity = value_obj.get("Quantity")
                items.append(
                    {
                        "item_name": desc.value_string if desc else "Unknown",
                        "price": float(price.value_currency.amount) if price and price.value_currency else 0.0,
                        "quantity": int(quantity.value_number) if quantity and quantity.value_number is not None else 1,
                    }
                )

        total_field = fields.get("Total") if fields else None
        total_amount = 0.0
        if total_field and total_field.value_currency:
            total_amount = float(total_field.value_currency.amount)

        date_field = fields.get("TransactionDate") if fields else None
        purchase_date = date_field.value_date.isoformat() if date_field and date_field.value_date else None

        merchant_field = fields.get("MerchantName") if fields else None
        store_name = merchant_field.value_string if merchant_field and merchant_field.value_string else "Unknown Store"

        return {
            "store_name": store_name,
            "purchase_date": purchase_date,
            "items": items,
            "total": total_amount,
            "raw": result.as_dict(),
        }
