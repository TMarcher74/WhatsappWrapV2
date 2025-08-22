from fastapi import APIRouter, UploadFile, File, HTTPException, status

from constants import Tags, MAX_UPLOAD_FILE_SIZE
from parser import Parser
import analyser


router = APIRouter()

@router.post("/analyse", tags=[Tags.Analyse])
async def anlayse_chat(
        file: UploadFile = File(...)
):
    # validate file
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

    raw_bytes = await file.read()
    chat_text = raw_bytes.decode("utf-8")  #, errors="ignore")
    
    # Sanitise data, remove names

    # Send it to AI

    # Send it to parser
    parser = Parser(chat_text)

    # Organize messages by user
    user_messages = {
        user: parser.get_messages_by_user(user)
        for user in parser.get_users()
    }

    # Run analysis
    analysis = {
        "users": parser.get_users(),
        "total_messages": analyser.get_messages_count(user_messages),
        "word_character_stats": analyser.get_word_char_count(user_messages),
        # "sum_of_total_messages":len(parser.get_messages()),
        "deleted_messages": analyser.get_messages_deleted_count(user_messages),
        "edited_messages": analyser.get_messages_edited_count(user_messages),
        "media": analyser.get_media_sent_count(user_messages),
        "top_words": analyser.get_most_used_words(parser.get_messages(), True, 10, 2),
        "message_date_time": {user: parser.get_date_time_by_user(user) for user in parser.get_users()},
        "emoji_count": analyser.get_emoji_count(user_messages),
    }

    return analysis

