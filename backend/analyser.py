import datetime
import re
from datetime import timedelta
from typing import Union
from emoji import is_emoji
import nltk
from nltk.corpus import stopwords
from collections import Counter
import statistics

nltk.download('stopwords')
custom_stopwords = {'media','omitted','message','deleted','edited','https','com'}

class Analyser:
    pass

def get_most_used_words(messages, stop_words: bool = True, top_n: int = 10, min_length: int = 2):
    """
    Gets the most frequently used words after filtering the stopwords if set to True
    """
    word_counter = Counter()
    stop_words_set = (set(stopwords.words('english')) | custom_stopwords) if stop_words else custom_stopwords

    for msg in messages:
        words = re.findall(r'\b\w+\b', msg.lower())
        filtered_words = [word for word in words if word not in stop_words_set and len(word) > min_length]
        word_counter.update(filtered_words)
    return dict(word_counter.most_common(top_n))

def get_messages_count(user_messages: dict, check_strings: Union[str, list[str]] = None) -> dict[str, int]:
    if isinstance(check_strings, str):
        check_strings = [check_strings]

    message_count = {}

    if check_strings is None:
        for user, messages in user_messages.items():
            count = 0
            for msg in messages:
                count += 1
            message_count[user] = count
        return message_count
    else:
        for user, messages in user_messages.items():
            count = 0
            for msg in messages:
                if any(check in msg for check in check_strings):
                    count += 1
            message_count[user] = count

    return message_count


def get_messages_deleted_count(user_messages: dict) -> dict[str:int]:
    """
    Gets the count of deleted messages by each user
    """
    deleted_messages = ["This message was deleted", "You deleted this message"]
    return get_messages_count(user_messages, deleted_messages)

def get_messages_edited_count(user_messages: dict) -> dict[str:int]:
    """
    Gets the count of edited messages by each user
    """
    edited_messages = "<This message was edited>"
    return get_messages_count(user_messages, edited_messages)

def get_media_sent_count(user_messages: dict) -> dict[str:int]:
    """
    Gets the count of media sent by each user
    """
    media_message = "<Media omitted>"
    return get_messages_count(user_messages, media_message)

def get_emoji_count(user_messages: dict) -> dict[str:list[int:dict[str:int]]]:
    """
    Get the count of emojis sent by a user
    """
    emoji_count = {}
    for user, messages in user_messages.items():
        count = 0
        emoji_freq = Counter()
        for msg in messages:
            for char in msg:
                if is_emoji(char):
                    count += 1
                    emoji_freq.update(char)
        emoji_count[user] = [count, dict(emoji_freq.most_common())]

    return emoji_count

def get_word_char_stats(user_messages: dict):
    """
    Get number of words and characters sent by a user
    """
    wc_stats = {}
    for user, messages in user_messages.items():
        w_count, c_count = 0,0
        words, chars = [], []
        for msg in messages:
            w_count += len(msg.split())
            c_count += len(msg)
            words.append(len(msg.split()))
            chars.append(len(msg))
        w_median = statistics.median(words)
        w_mean = int(statistics.mean(words))
        w_mode = statistics.mode(words)
        c_median = statistics.median(chars)
        c_mean = int(statistics.mean(chars))
        c_mode = statistics.mode(chars)
        wc_stats[user] = {
            "words": w_count,
            "characters":c_count,
            "word_median": w_median,
            "word_mean":w_mean,
            "word_mode": w_mode,
            "chars_median": c_median,
            "chars_mean": c_mean,
            "chars_mode": c_mode
        }

    return wc_stats

def get_top_convos(
        date_times: list[datetime],
        messages: list[str],
        users: list[str],
        min_convo_time: int = 3,
        min_convo_length: int = 10,
        top_n: int = 5
):
    START_CONV = datetime.timedelta(minutes=5)
    CONT_CONV = datetime.timedelta(minutes=2)

    i = 0
    all_conversations, longest_conversation, most_messages_conversation = [], [], []
    longest_duration = timedelta(seconds=0)
    most_messages = 0
    while i < len(date_times)-1:
        conversation = []
        if date_times[i+1] - date_times[i] <= START_CONV:
            start = date_times[i]
            conversation.append([start, users[i], messages[i]])
            i += 1
            while i+1 < len(date_times) and date_times[i+1] - date_times[i] <= CONT_CONV:
                conversation.append([date_times[i], users[i], messages[i]])
                i += 1

            conversation.append([date_times[i], users[i], messages[i]])
            end = date_times[i]

            conv_duration = end - start + timedelta(seconds=60)
            message_count = len(conversation)
            if conv_duration > longest_duration:
                longest_duration = conv_duration
                longest_conversation = [{longest_duration.seconds/60:conversation}]
            if message_count > most_messages:
                most_messages = message_count
                most_messages_conversation = [{most_messages: conversation}]
            if conv_duration.seconds > min_convo_time * 60 and message_count > min_convo_length:
                messages_per_minute = message_count/(conv_duration.seconds/60)
                all_conversations.append({messages_per_minute:conversation})
        i+=1

    all_conversations.sort(key=lambda x: next(iter(x)), reverse=True)
    return {"Longest conversation in minutes":longest_conversation,
            "Most messages sent in a conversation":most_messages_conversation,
            "Messages per minute":all_conversations[:top_n]}

def get_longest_streak(dates: list[datetime.date]):
    i, streak, count = 0, 0, 0
    streak_start, streak_end = 0, 0
    dates = list(set(dates))
    dates.sort()
    while i in range(0,len(dates)-1):
        count = 0
        start = dates[i]
        while dates[i+1] - dates[i] <= datetime.timedelta(days=1):
            count += 1
            i += 1
        else:
            end = dates[i]
        if count > streak:
            streak_start = start
            streak_end = end
            streak = count
        i += 1

    return {"Streak start": streak_start, "Streak end": streak_end, "Streak in days":streak}
