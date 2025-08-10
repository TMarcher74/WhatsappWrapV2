from fastapi import APIRouter, UploadFile, File, HTTPException, status

from constants import Tags, MAX_UPLOAD_FILE_SIZE
from parser import Parser
import analyser


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
    
    raw_bytes = await file.read()
    chat_text = raw_bytes.decode("utf-8")  #, errors="ignore")
    x = Parser(chat_text)
    messages = x.get_messages()
    return analyser.get_most_used_words(messages, 30)


    return chat_text  # For now, just return the text