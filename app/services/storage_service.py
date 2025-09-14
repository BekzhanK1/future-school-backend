import os
import uuid
from pathlib import Path
from fastapi import UploadFile


def get_storage_dir() -> Path:
    base = os.getenv("STORAGE_DIR", "./data/uploads")
    path = Path(base)
    path.mkdir(parents=True, exist_ok=True)
    return path


async def save_upload(file: UploadFile, subdir: str | None = None) -> str:
    storage_root = get_storage_dir()
    target_dir = storage_root / subdir if subdir else storage_root
    target_dir.mkdir(parents=True, exist_ok=True)

    ext = Path(file.filename).suffix if file.filename else ""
    name = f"{uuid.uuid4().hex}{ext}"
    dest = target_dir / name

    # Stream to disk
    with dest.open("wb") as out:
        while True:
            chunk = await file.read(1024 * 1024)
            if not chunk:
                break
            out.write(chunk)

    await file.close()
    return str(dest)



