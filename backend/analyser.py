import re
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

def get_word_char_count(user_messages: dict):
    """
    Get number of words and characters sent by a user
    """
    wc_count = {}
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
        wc_count[user] = {
            "words": w_count,
            "characters":c_count,
            "word_median": w_median,
            "word_mean":w_mean,
            "word_mode": w_mode,
            "chars_median": c_median,
            "chars_mean": c_mean,
            "chars_mode": c_mode
        }

    return wc_count

