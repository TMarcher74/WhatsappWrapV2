import datetime
import re
from datetime import timedelta, datetime
from typing import Union
from xmlrpc.client import DateTime

from emoji import is_emoji
import nltk
from nltk.corpus import stopwords
from collections import Counter, defaultdict
import statistics
from urllib.parse import urlparse
from constants import DOMAIN_MAPS, SysMsgActions

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

def find_emoticons_dict(text):
    emoticons_pattern = re.compile(
    r"""(?<!\S)                           # no non-space before
    (?:
        [:=;]-?[\)DPO3/\\]     # :) :-) :D :-D :P :-P :3 :-3 :/ :-/
      | [:=]-?\(               # :( :-(
      | [:=]'-?\(              # :'( :'-(
      | [:=]-?[oO0]            # :o :-o :O :-O :0
      | [:=]-?[sS]             # :s :-s :S :-S
      | [:=]-?[@$]             # :@ :-@ :$ :-$
      | [:=]-?[\|]             # :| :-|
      | ;[-]?[)D]              # ;) ;-) ;D ;-D
      | xD|XD                  # xD XD
      | <3                     # <3 heart
      | :"\)                   # :")
      | :"\(                   # :"(
      | :'\(                   # :'(
      | :'\)                   # :')
    )
    (?!\S)                     # no non-space after
    """,
    re.VERBOSE
)
    found_emoticons = re.findall(emoticons_pattern, text)
    count = len(found_emoticons)

    return count, found_emoticons

def get_emoji_emoticon_count(user_messages: dict) -> dict[str:list[int:dict[str:int]]]:
    """
    Get the count of emojis sent by a user
    """
    emoji_counter, emoticon_counter = {}, {}
    for user, messages in user_messages.items():
        emoji_count = 0
        emoji_freq = Counter()
        emoticon_count= 0
        emoticon_freq = Counter()
        for msg in messages:
            for char in msg:
                if is_emoji(char):
                    emoji_count += 1
                    emoji_freq.update(char)
            a, b = find_emoticons_dict(msg)
            emoticon_count += a
            emoticon_freq.update(b)
        emoji_counter[user] = [emoji_count, dict(emoji_freq.most_common())]
        emoticon_counter[user] = [emoticon_count, dict(emoticon_freq.most_common())]

    return emoji_counter, emoticon_counter

def classify_url(raw_url: str) -> str:
    try:
        parsed = urlparse(raw_url)
        domain = parsed.netloc.lower()
        if domain.startswith("www."):
            domain = domain[4:]
        for platform, domains in DOMAIN_MAPS.items():
            if any(domain == d or domain.endswith("." + d) for d in domains):
                return platform
        return domain
    except Exception:
        return "other"

def get_links(user_messages: dict):
    url_pattern = re.compile(r"https?://\S+")
    url_count = {}

    for user, messages in user_messages.items():
        urls = []
        count = defaultdict(int)
        for msg in messages:
            found_urls = url_pattern.findall(msg)
            for raw_url in found_urls:
                platform = classify_url(raw_url)
                urls.append(raw_url)
                count[platform] += 1
        sorted_count = dict(sorted(count.items(), key=lambda x: x[1], reverse=True))
        url_count[user] = [sorted_count,urls]

    return url_count

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
        min_convo_time: int = 5,
        min_convo_length: int = 20,
        top_n: int = 5
):
    combined = sorted(zip(date_times, users, messages), key=lambda x: x[0])
    date_times, users, messages = zip(*combined)

    gaps = [(date_times[i + 1] - date_times[i]).total_seconds()
            for i in range(len(date_times) - 1)]
    if not gaps:
        return {}

    sorted_gaps = sorted(gaps)
    idx = int(0.9 * len(sorted_gaps)) # 90th percentile of gaps
    T = sorted_gaps[idx]
    T = max(120, min(1800, T))  # clamp between 120s and 1800s
    gap_thresh = timedelta(seconds=T)

    #group into conversations (rolling window)
    conversations = []
    current_conv = [(date_times[0], users[0], messages[0])]
    for i in range(1, len(date_times)):
        gap = date_times[i] - date_times[i - 1]
        if gap <= gap_thresh:
            current_conv.append((date_times[i], users[i], messages[i]))
        else:
            conversations.append(current_conv)
            current_conv = [(date_times[i], users[i], messages[i])]
    if current_conv:
        conversations.append(current_conv)

    #analyze conversations
    all_conversations = []
    longest_conversation = None
    most_messages_conversation = None
    longest_duration = timedelta(seconds=0)
    most_messages = 0

    for conv in conversations:
        start = conv[0][0]
        end= conv[-1][0]
        duration = end - start
        msgs = len(conv)
        participants = set(u for ts, u, msg in conv)

        # filter short convos
        if duration.total_seconds() < min_convo_time * 60 or msgs < min_convo_length:
            continue

        mpm = msgs / max(duration.total_seconds() / 60, 1)  # messages per min
        upm = len(participants) / max(duration.total_seconds() / 60, 1)  # unique participants per min

        convo_stats = {
            "start": start,
            "end": end,
            "duration_min": duration.total_seconds() / 60,
            "messages": msgs,
            "participants": participants,
            "messages_per_min": mpm,
            "unique_participants_per_min": upm,
            "conversation": conv
        }
        all_conversations.append(convo_stats)

        # track longest & busiest
        if duration > longest_duration:
            longest_duration = duration
            longest_conversation = convo_stats
        if msgs > most_messages:
            most_messages = msgs
            most_messages_conversation = convo_stats

    return {
        "gap_threshold_seconds": gap_thresh.total_seconds(),
        "Longest conversation": longest_conversation,
        "Most messages conversation": most_messages_conversation,
        f"Top {top_n} by messages / min":
            sorted(all_conversations, key=lambda x: x["messages_per_min"], reverse=True)[:top_n],
        f"Top {top_n} by messages / min * unique participants / min":
            sorted(all_conversations, key=lambda x: x["messages_per_min"] * x["unique_participants_per_min"], reverse=True)[:top_n],
    }

def get_longest_streak(dates: list[datetime.date]):
    i, streak, count = 0, 0, 0
    streak_start, streak_end = 0, 0
    dates = list(set(dates))
    dates.sort()
    while i in range(0,len(dates)-1):
        count = 0
        start = dates[i]
        while dates[i+1] - dates[i] <= timedelta(days=1):
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


def _to_datetime(date: datetime.date, time: datetime.time):
    return datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M:%S")

def get_group_creation(system_messages: list[dict]):
    for msg in system_messages:
            if msg["action"] == SysMsgActions.CreateGroup:
                return msg["date"], msg["time"], msg["author"], msg["action"]

def get_nth_message(user_messages:list[dict], n: int):
    for i in range(1,len(user_messages)):
        if i==n:
            return (user_messages[n]["date"],
                    user_messages[n]["time"],
                    user_messages[n]["sender"],
                    user_messages[n]["message"])

def get_user_first_message(user_messages:list[dict], user: str):
    for msg in user_messages:
        if msg["sender"] is user:
            return msg

def get_user_joins(user_messages:list[dict], system_messages: list[dict], user_list: list[str]):
    user_joins = {}
    mod_user_list = user_list.copy()
    for msg in system_messages:
        if msg["action"] == SysMsgActions.AddUser:
            if msg["added"] in mod_user_list:
                user_joins.update({f"{msg["added"]}":_to_datetime(msg["date"], msg["time"])})
                mod_user_list.remove(msg["added"])
        if msg["action"] == SysMsgActions.CreateGroup:
            user_joins.update({f"{msg["author"]}": "Created the group, hence the first to join."})
            mod_user_list.remove(msg["author"])


    for user in user_list:
        if user_joins.get(user) and hasattr(user_joins[user], "date"):
            # For those that joined before the group was created, set it as when the group was created
            if user_joins[user].date() > get_user_first_message(user_messages, user)["date"]:
                user_joins[user] = "Joined before you, hence no log of it."
        elif user not in user_joins.keys():
            date, time, _, _ = get_group_creation(system_messages)
            user_joins[user] = _to_datetime(date, time)

    user_joins = ((b,f"{a} has joined the chat") for a,b in user_joins.items())
    return user_joins

def get_milestones(
        user_messages:list[dict],
        system_messages:list[dict],
        user_list: list[str],
        is_group: bool
):
    """
    Thinking of adding stuff like 
    - When the group was created and by whom, done
    - When each person of the group joined, all that stuff, done
    - When each person sent their first message and what it was, done
    - 100th / 1000th / 10000th message, done
    - Most active day
    - Longest convo
    - Message spikes, unusually high traffic signals a big event
    - X no.of days for next anniversary or since prev one
    - ??
    """
    grp_milestones = []
    chat_milestones = []

    # date, time, sender, author, action, message = None, None, None, None, None, None
    if is_group:
        # Group creation
        date, time, author, action = get_group_creation(system_messages)
        grp_milestones.append((_to_datetime(date, time), f"The group was created by {author}"))

        #When each member joined
        for _ in get_user_joins(user_messages, system_messages, user_list):
            grp_milestones.append(_)

    # First message sent by each user
    for user in user_list:
        _ = get_user_first_message(user_messages, user)
        date, time, sender, message = _["date"], _["time"], _["sender"], _["message"]
        chat_milestones.append((_to_datetime(date, time), f"The 1st message sent by {sender} : {message}"))

    # Add every 100th, 1000th, 10000th... message to the milestone
    i=99
    while i <= len(user_messages):
        date, time, sender, message = get_nth_message(user_messages, i)
        chat_milestones.append((_to_datetime(date, time), f"The {i}th message was sent by {sender} : {message}"))
        if i % 10 == 1:
            i-=1
            i*=10
            i-=1
        else: i+=1

    for _ in grp_milestones:
        chat_milestones.append(_)

    return chat_milestones

def get_day_wise_frequency():
    pass

def get_time_wise_frequency():
    pass