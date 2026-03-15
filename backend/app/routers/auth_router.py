import uuid

from fastapi import APIRouter, Depends
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.repositories.user_repository import UserRepository


router = APIRouter(prefix="/auth", tags=["auth"])


class RegisterRequest(BaseModel):
    email: EmailStr


class RegisterResponse(BaseModel):
    user_id: uuid.UUID
    email: EmailStr


@router.post("/register", response_model=RegisterResponse)
def register(payload: RegisterRequest, db: Session = Depends(get_db)) -> RegisterResponse:
    repo = UserRepository(db)
    user = repo.get_or_create_by_email(str(payload.email))
    return RegisterResponse(user_id=user.id, email=user.email)
