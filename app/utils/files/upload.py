from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import UploadFile


def _sanitize_filename(filename: str) -> str:
    safe_chars = "-_.() "
    sanitized = "".join(c for c in filename if c.isalnum() or c in safe_chars)
    return sanitized or "file"


def _build_upload_dir(
    base_dir: Path, session_id: Optional[int], document_id: Optional[int]
) -> Path:
    parts: List[str] = []
    if session_id is not None:
        parts.append(f"session_{session_id}")
    if document_id is not None:
        parts.append(f"document_{document_id}")
    target = base_dir.joinpath(*parts) if parts else base_dir
    target.mkdir(parents=True, exist_ok=True)
    return target


def _save_upload_file_to_path(source: UploadFile, destination_path: Path) -> int:
    bytes_written = 0
    with destination_path.open("wb") as out_file:
        while True:
            chunk = source.file.read(1024 * 1024)
            if not chunk:
                break
            out_file.write(chunk)
            bytes_written += len(chunk)
    return bytes_written


def save_uploaded_files(
    uploaded_files: List[UploadFile],
    session_id: Optional[int],
    document_id: Optional[int],
    base_dir: Path | str = "uploads",
) -> List[Dict[str, Any]]:
    
    base_path = Path(base_dir)
    target_dir = _build_upload_dir(base_path, session_id, document_id)

    saved: List[Dict[str, Any]] = []
    for file in uploaded_files:
        original_name = file.filename or "file"
        sanitized_name = _sanitize_filename(original_name)
        destination = target_dir / sanitized_name
        size = _save_upload_file_to_path(file, destination)
        saved.append(
            {
                "original_filename": original_name,
                "stored_filename": sanitized_name,
                "content_type": file.content_type,
                "size": size,
                "path": str(destination.resolve()),
            }
        )
    return saved
