import re
from typing import Union

import nltk
from nltk.corpus import stopwords
from collections import Counter

nltk.download('stopwords')
custom_stopwords = {'media','omitted','message','deleted','edited','https','com'}

class Analyser:
    pass

def get_most_used_words(messages, stop_words: bool = True, top_n: int = 10):
    """
    Gets the most frequently used words after filtering the stopwords if set to True
    """
    word_counter = Counter()
    stop_words_set = (set(stopwords.words('english')) | custom_stopwords) if stop_words else custom_stopwords

    for msg in messages:
        words = re.findall(r'\b\w+\b', msg.lower())
        filtered_words = [word for word in words if word not in stop_words_set]
        word_counter.update(filtered_words)
    return word_counter.most_common(top_n)

def get_messages_count(user_messages: dict, check_strings: Union[str, list[str]]) -> dict[str, int]:
    if isinstance(check_strings, str):
        check_strings = [check_strings]

    message_count = {}

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