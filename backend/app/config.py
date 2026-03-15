from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Receipt Intelligence API"
    app_version: str = "0.1.0"
    api_prefix: str = "/api"
    cors_origins: list[str] = ["http://localhost:5173"]

    database_url: str = "postgresql+psycopg2://postgres:postgres@localhost:5432/expenses"

    azure_blob_connection_string: str = ""
    azure_blob_container_name: str = "user-receipts"

    azure_docintel_endpoint: str = ""
    azure_docintel_key: str = ""

    environment: str = "development"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
