from fastapi import APIRouter, UploadFile, File, HTTPException, status
from constants import Tags, MAX_UPLOAD_FILE_SIZE, file_cache
from fastapi.params import Query
from parser import Parser
import analyser

router = APIRouter(prefix="/analyse")

def verify_parsed_data(file_id: str):
    parsed_data = file_cache.get(file_id)
    if not parsed_data:
        print(file_cache)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File expired or not found"
        )
    return parsed_data

def get_user_messages(parsed_data: Parser):
    user_messages = {
        user: parsed_data.get_messages_by_user(user)
        for user in parsed_data.get_users()
    }
    return user_messages

# Users
@router.get("/users/{file_id}", tags=[Tags.Analyse_Users])
async def get_users(file_id: str):
    parsed_data = verify_parsed_data(file_id)
    return {"users": parsed_data.get_users(),}

# Messages
@router.get("/messages/{file_id}/total", tags=[Tags.Analyse_Messages])
async def get_total_messages(file_id: str):
    parsed_data = verify_parsed_data(file_id)
    user_messages = get_user_messages(parsed_data)
    return {"total_messages": analyser.get_messages_count(user_messages),}

@router.get("/messages/{file_id}/stats", tags=[Tags.Analyse_Messages])
async def get_message_stats(file_id: str):
    parsed_data = verify_parsed_data(file_id)
    user_messages = get_user_messages(parsed_data)
    return {"word_char_stats": analyser.get_word_char_stats(user_messages),}

@router.get("/messages/{file_id}/deleted", tags=[Tags.Analyse_Messages])
async def get_deleted_messages(file_id: str):
    parsed_data = verify_parsed_data(file_id)
    user_messages = get_user_messages(parsed_data)
    return {"deleted_messages": analyser.get_ratioed(analyser.get_messages_count(user_messages),
                                                     analyser.get_messages_deleted_count(user_messages)),}

@router.get("/messages/{file_id}/edited", tags=[Tags.Analyse_Messages])
async def get_edited_messages(file_id: str):
    parsed_data = verify_parsed_data(file_id)
    user_messages = get_user_messages(parsed_data)
    return {"edited_messages": analyser.get_ratioed(analyser.get_messages_count(user_messages),
                                                    analyser.get_messages_edited_count(user_messages)),}

@router.get("/messages/{file_id}/media", tags=[Tags.Analyse_Messages])
async def get_media(file_id: str):
    parsed_data = verify_parsed_data(file_id)
    user_messages = get_user_messages(parsed_data)
    return {"media": analyser.get_ratioed(analyser.get_messages_count(user_messages),
                                          analyser.get_media_sent_count(user_messages)),}

@router.get("/messages/{file_id}/links", tags=[Tags.Analyse_Messages])
async def get_links(file_id: str):
    parsed_data = verify_parsed_data(file_id)
    user_messages = get_user_messages(parsed_data)
    url_count, detailed_url_count = analyser.get_links(user_messages)
    return {"url_count": analyser.get_ratioed(analyser.get_messages_count(user_messages),
                                              url_count),
            "detailed_url_count": detailed_url_count}

@router.get("/messages/{file_id}/emojis-emoticons", tags=[Tags.Analyse_Messages])
async def get_emojis_emoticons(file_id: str):
    parsed_data = verify_parsed_data(file_id)
    user_messages = get_user_messages(parsed_data)
    return {"emoji_emoticon_count": analyser.get_emoji_emoticon_count(user_messages),}

@router.get("/messages/{file_id}/top_words", tags=[Tags.Analyse_Messages])
async def get_top_words(
        file_id: str,
        top_n: int = Query(30, ge = 1, le = 100, description = "Number of top words to return"),
        min_length: int = Query(2, ge = 1, description = "Minimum word length to include"),
        stop_words: bool = Query(True, description = "Whether to exclude stopwords")
):
    parsed_data = verify_parsed_data(file_id)
    return {"top_words": analyser.get_most_used_words(parsed_data.get_messages_by_user(), stop_words, top_n, min_length),}

# Time
@router.get("/time/{file_id}/streak", tags=[Tags.Analyse_Time])
async def get_longest_streak(file_id: str):
    parsed_data = verify_parsed_data(file_id)
    return {"longest_streak": analyser.get_longest_streak(parsed_data.get_date_by_user()),}

@router.get("/time/{file_id}/day-frequency", tags=[Tags.Analyse_Time])
async def get_day_freq(
        file_id: str,
        user_wise: bool = Query(False, description= "Gives result with respect to each user")
):
    parsed_data = verify_parsed_data(file_id)
    if user_wise: return {"day_frequency": {user: analyser.get_day_wise_freq(parsed_data.get_date_by_user(user))
                                            for user in parsed_data.get_users()}},
    return {"day_frequency": analyser.get_day_wise_freq(parsed_data.get_date_by_user()),}

@router.get("/time/{file_id}/date-frequency", tags=[Tags.Analyse_Time])
async def get_date_freq(
        file_id: str,
        user_wise: bool = Query(False, description= "Gives result with respect to each user")
):
    parsed_data = verify_parsed_data(file_id)
    if user_wise: return {"date_frequency": {user: analyser.get_date_wise_freq(parsed_data.get_date_by_user(user))
                                            for user in parsed_data.get_users()}},
    return {"date_frequency": analyser.get_date_wise_freq(parsed_data.get_date_by_user())}

@router.get("/time/{file_id}/time-frequency", tags=[Tags.Analyse_Time])
async def get_time_freq(
        file_id: str,
        user_wise: bool = Query(False, description= "Gives result with respect to each user")
):
    parsed_data = verify_parsed_data(file_id)
    if user_wise: return {"date_frequency": {user: analyser.get_time_wise_freq(parsed_data.get_time_by_user(user))
                                             for user in parsed_data.get_users()}},
    return {"time_frequency": analyser.get_time_wise_freq(parsed_data.get_time_by_user()),}

@router.get("/time/{file_id}/detailed-date-frequency", tags=[Tags.Analyse_Time])
async def get_detailed_date_freq(
        file_id: str,
):
    parsed_data = verify_parsed_data(file_id)
    user_messages = {
        user: parsed_data.get_date_and_messages_by_user(user)
        for user in parsed_data.get_users()
    }

    return {"detailed_frequency": analyser.get_detailed_timeseries(parsed_data.get_date_by_user(), user_messages),}

# Events
@router.get("/events/{file_id}/milestones", tags=[Tags.Analyse_Events])
async def get_milestones(
        file_id: str,
        min_convo_time: int = Query(5, ge=1, description= "Minimum conversation time in min"),
        min_convo_length: int = Query(20, ge=1, description= "Minimum number of messages"),
        top_n: int = Query(5, ge=1, description= "Returns top n number of convos")
):
    parsed_data = verify_parsed_data(file_id)
    return {
        "milestones":
        analyser.get_milestones(
            parsed_data.user_messages,
            parsed_data.system_messages,
            parsed_data.get_users(),
            parsed_data.get_date_by_user(),
            analyser.get_top_convos(
                parsed_data.get_date_time_by_user(),
                parsed_data.get_messages_by_user(),
                parsed_data.get_users_wrt_messages(),
                min_convo_time,
                min_convo_length,
                top_n
            ),
            analyser.get_longest_streak(parsed_data.get_date_by_user()),
            parsed_data.is_group(),
        )
    }

@router.get("/events/{file_id}/top-convos", tags=[Tags.Analyse_Events])
async def get_top_convos(
        file_id: str,
        min_convo_time: int = Query(5, ge=1, description= "Minimum conversation time in min"),
        min_convo_length: int = Query(20, ge=1, description= "Minimum number of messages"),
        top_n: int = Query(5, ge=1, description= "Returns top n number of convos")
):
    parsed_data = verify_parsed_data(file_id)
    return {
        "top_convos":
        analyser.get_top_convos(
            parsed_data.get_date_time_by_user(),
            parsed_data.get_messages_by_user(),
            parsed_data.get_users_wrt_messages(),
            min_convo_time,
            min_convo_length,
            top_n
        )
    }

@router.get("/events/{file_id}/responses", tags=[Tags.Analyse_Events])
async def get_responses(file_id: str):
    parsed_data = verify_parsed_data(file_id)
    user_messages = get_user_messages(parsed_data)
    return {"response_map": analyser.normalise_reply_map(analyser.get_user_reply_map(parsed_data.get_users_wrt_messages()),
                                                         analyser.get_messages_count(user_messages))}


@router.post("/all/{file_id}")
async def anlayse_all(file_id: str):
    # Retrieve parsed data from cache
    parsed_data = verify_parsed_data(file_id)

    # Organize messages by user
    user_messages = {
        user: parsed_data.get_messages_by_user(user)
        for user in parsed_data.get_users()
    }

    # Run analysis
    analysis = {
        "users": parsed_data.get_users(),
        "total_messages": analyser.get_messages_count(user_messages),
        "word_character_stats": analyser.get_word_char_stats(user_messages),
        # "sum_of_total_messages":len(parser.get_messages()),
        "deleted_messages": analyser.get_messages_deleted_count(user_messages),
        "edited_messages": analyser.get_messages_edited_count(user_messages),
        "media": analyser.get_media_sent_count(user_messages),
        "links": analyser.get_links(user_messages),
        "top_words": analyser.get_most_used_words(parsed_data.get_messages_by_user(), stop_words = True, top_n = 30, min_length = 2),
        "emoji_count": analyser.get_emoji_emoticon_count(user_messages),
        "longest_streak": analyser.get_longest_streak(parsed_data.get_date_by_user()),
        "day_frequency": analyser.get_day_wise_freq(parsed_data.get_date_by_user()),
        "time_frequency": analyser.get_time_wise_freq(parsed_data.get_time_by_user()),
        "date_frequency": analyser.get_date_wise_freq(parsed_data.get_date_by_user()),
        "detailed_frequency": analyser.get_detailed_timeseries(parsed_data.get_date_by_user(), user_messages),
        "user_wise_day_frequency": {user: analyser.get_day_wise_freq(parsed_data.get_date_by_user(user)) for user in parsed_data.get_users()},
        "user_wise_time_frequency": {user: analyser.get_time_wise_freq(parsed_data.get_time_by_user(user)) for user in parsed_data.get_users()},
        "milestones": analyser.get_milestones(
            parsed_data.user_messages,
            parsed_data.system_messages,
            parsed_data.get_users(),
            parsed_data.get_date_by_user(),
            analyser.get_top_convos(parsed_data.get_date_time_by_user(),parsed_data.get_messages_by_user(),parsed_data.get_users_wrt_messages(),
                min_convo_time=5,
                min_convo_length=20,
                top_n=5
            ),
            analyser.get_longest_streak(parsed_data.get_date_by_user()),
            parsed_data.is_group(),
        ),
        "convos": analyser.get_top_convos(
            parsed_data.get_date_time_by_user(),
            parsed_data.get_messages_by_user(),
            parsed_data.get_users_wrt_messages(),
                min_convo_time=5,
                min_convo_length=20,
                top_n=5
        ),
    }

    return analysis

