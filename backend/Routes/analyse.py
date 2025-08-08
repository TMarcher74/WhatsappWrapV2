from fastapi import APIRouter, UploadFile, File, HTTPException, status

from constants import Tags, MAX_UPLOAD_FILE_SIZE


router = APIRouter()

@router.post("/analyse", tags=[Tags.Analyse])
async def anlayse_chat(
        file: UploadFile = File(...)
):
    if file.content_type != "text/plain":
        raise HTTPException(
            status_code = status.HTTP_406_NOT_ACCEPTABLE,
            detail = "Wrong file type uploaded, only text files are accepted"
        )
    if file.size > MAX_UPLOAD_FILE_SIZE:
        raise HTTPException(
            status_code = status.HTTP_406_NOT_ACCEPTABLE,
            detail = "File size exceeds 18MB"
        )

    # Sanitise data, remove names

    # Send it to AI

    # Send it to parser

    else:
        contents = await file.read()

        return file