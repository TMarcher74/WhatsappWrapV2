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
        "word_character_stats": analyser.get_word_char_stats(user_messages),
        # "sum_of_total_messages":len(parser.get_messages()),
        "deleted_messages": analyser.get_messages_deleted_count(user_messages),
        "edited_messages": analyser.get_messages_edited_count(user_messages),
        "media": analyser.get_media_sent_count(user_messages),
        "links": analyser.get_links(user_messages),
        "top_words": analyser.get_most_used_words(parser.get_messages_by_user(), stop_words = True, top_n = 30, min_length = 2),
        "emoji_count": analyser.get_emoji_emoticon_count(user_messages),
        "longest_streak": analyser.get_longest_streak(parser.get_date_by_user()),
        "convos": analyser.get_top_convos(
            parser.get_date_time_by_user(),
            parser.get_messages_by_user(),
            parser.get_users_wrt_messages(),
            min_convo_time = 5,
            min_convo_length = 20,
            top_n = 5
        ),
        "milestones": analyser.get_milestones(parser.user_messages, parser.system_messages, parser.get_users(), parser.is_group()),
        # "message_date_time": {user: parser.get_date_time_by_user(user) for user in parser.get_users()},
    }

    return analysis

