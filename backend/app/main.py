from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database.db import init_db
from app.routers import analytics_router, auth_router, health_router, insights_router, receipt_router


app = FastAPI(title=settings.app_name, version=settings.app_version)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    if settings.environment == "development":
        init_db()


app.include_router(auth_router.router, prefix=settings.api_prefix)
app.include_router(receipt_router.router, prefix=settings.api_prefix)
app.include_router(insights_router.router, prefix=settings.api_prefix)
app.include_router(analytics_router.router, prefix=settings.api_prefix)
app.include_router(health_router.router, prefix=settings.api_prefix)
