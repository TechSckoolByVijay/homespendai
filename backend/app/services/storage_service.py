import uuid
from pathlib import Path

from azure.core.exceptions import ResourceExistsError
from azure.storage.blob import BlobServiceClient

from app.config import settings


class StorageService:
    def __init__(self) -> None:
        self.container = settings.azure_blob_container_name
        self.client = None
        if settings.azure_blob_connection_string:
            blob_client = BlobServiceClient.from_connection_string(settings.azure_blob_connection_string)
            self.client = blob_client.get_container_client(self.container)

    def upload_receipt(self, user_id: uuid.UUID, file_name: str, content: bytes, content_type: str) -> str:
        safe_file_name = Path(file_name).name
        blob_name = f"users/{user_id}/receipts/{uuid.uuid4()}-{safe_file_name}"
        if self.client is None:
            return f"https://local.blob/{self.container}/{blob_name}"

        try:
            self.client.create_container()
        except ResourceExistsError:
            pass

        self.client.upload_blob(
            name=blob_name,
            data=content,
            overwrite=True,
            content_type=content_type,
        )
        return f"{self.client.url}/{blob_name}"
