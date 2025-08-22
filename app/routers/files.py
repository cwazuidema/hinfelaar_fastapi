from typing import List, Optional

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.utils.files.upload import save_uploaded_files


router = APIRouter(tags=["Files"])


@router.post("/upload")
async def upload_files(
    file: List[UploadFile] = File(..., description="One or more files to upload"),
    sessionId: Optional[int] = Form(None),
    documentId: Optional[int] = Form(None),
):
    if not file:
        raise HTTPException(status_code=400, detail={"error": "No files uploaded"})

    saved = save_uploaded_files(file, sessionId, documentId)

    return {
        "success": True,
        "count": len(saved),
        "sessionId": sessionId,
        "documentId": documentId,
        "files": saved,
    }
