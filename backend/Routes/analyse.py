from fastapi import APIRouter, UploadFile, File, HTTPException, status

from backend.constants import Tags, MAX_UPLOAD_FILE_SIZE


router = APIRouter()

@router.post("/analyse", tags=[Tags.Analyse])
async def anlayse_chat(
        file: UploadFile = File(...)
):
    if file.content_type != "text/plain":
        raise HTTPException(
            status_code = status.HTTP_406_NOT_ACCEPTABLE,
            detail = "Wrong file type uploaded, only .txt is accepted"
        )
    if file.size > MAX_UPLOAD_FILE_SIZE:
        raise HTTPException(
            status_code = status.HTTP_406_NOT_ACCEPTABLE,
            detail = "File size exceeds 18MB"
        )

    # Send it to parser

    else:
        return file