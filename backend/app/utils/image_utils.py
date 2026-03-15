from pathlib import Path


def guess_content_type(filename: str) -> str:
    suffix = Path(filename).suffix.lower()
    if suffix in {".jpg", ".jpeg"}:
        return "image/jpeg"
    if suffix == ".png":
        return "image/png"
    if suffix == ".pdf":
        return "application/pdf"
    return "application/octet-stream"
