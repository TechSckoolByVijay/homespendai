import uuid

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.receipt_schema import ReceiptDeleteResponse, ReceiptResponse, ReceiptUpload
from app.services.receipt_service import ReceiptService


router = APIRouter(prefix="/receipts", tags=["receipts"])


def _to_response_model(receipt) -> ReceiptResponse:
    return ReceiptResponse(
        id=receipt.id,
        store_name=receipt.store_name,
        purchase_date=receipt.purchase_date,
        total_amount=float(receipt.total_amount or 0),
        image_url=receipt.image_url,
        items=[
            {
                "item_name": item.item_name,
                "category": item.category,
                "price": float(item.price or 0),
                "quantity": item.quantity,
            }
            for item in receipt.items
        ],
    )


@router.post("/upload", response_model=ReceiptResponse)
async def upload_receipt(
    payload: ReceiptUpload = Depends(),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
) -> ReceiptResponse:
    service = ReceiptService(db)
    receipt = await service.upload_and_process(payload.user_id, file)
    return _to_response_model(receipt)


@router.get("", response_model=list[ReceiptResponse])
def list_receipts(user_id: uuid.UUID, db: Session = Depends(get_db)) -> list[ReceiptResponse]:
    service = ReceiptService(db)
    return [_to_response_model(receipt) for receipt in service.list_receipts(user_id)]


@router.get("/{receipt_id}", response_model=ReceiptResponse)
def get_receipt(receipt_id: uuid.UUID, db: Session = Depends(get_db)) -> ReceiptResponse:
    service = ReceiptService(db)
    receipt = service.get_receipt(receipt_id)
    if not receipt:
        raise HTTPException(status_code=404, detail="Receipt not found")
    return _to_response_model(receipt)


@router.delete("/{receipt_id}", response_model=ReceiptDeleteResponse)
def delete_receipt(receipt_id: uuid.UUID, db: Session = Depends(get_db)) -> ReceiptDeleteResponse:
    service = ReceiptService(db)
    deleted = service.delete_receipt(receipt_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Receipt not found")
    return ReceiptDeleteResponse(message="Receipt deleted")
