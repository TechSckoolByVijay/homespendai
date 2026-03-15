from app.database.base import Base
from app.database.session import engine


def init_db() -> None:
    from app.models import insight_model, item_model, receipt_model, user_model  # noqa: F401

    Base.metadata.create_all(bind=engine)
