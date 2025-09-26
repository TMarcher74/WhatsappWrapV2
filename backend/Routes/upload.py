from fastapi import APIRouter, UploadFile, File, HTTPException, status
from constants import Tags, MAX_UPLOAD_FILE_SIZE, file_cache
from parser import Parser
import  uuid


router = APIRouter()

@router.post("/upload", tags=[Tags.Upload])
async def upload_chat(file: UploadFile = File(...)):
    # validate file
    if file.content_type != "text/plain":
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Only .txt files are accepted"
        )
    if file.size > MAX_UPLOAD_FILE_SIZE:
        raise HTTPException(
            status_code = status.HTTP_406_NOT_ACCEPTABLE,
            detail = "File size exceeds 18MB"
        )

    raw_bytes = await file.read()
    chat_text = raw_bytes.decode("utf-8") #, errors="ignore")
    parsed_data = Parser(chat_text)

    file_id = str(uuid.uuid4())
    file_cache[file_id] = parsed_data

    return {"file_id": file_id, "message": "File uploaded to cache successfully"}