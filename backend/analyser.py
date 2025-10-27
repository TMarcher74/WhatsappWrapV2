import datetime
import re
from datetime import timedelta, datetime, time
from emoji import is_emoji
import nltk
from nltk.corpus import stopwords
from collections import Counter, defaultdict
import statistics
from urllib.parse import urlparse
from constants import DOMAIN_MAPS, SysMsgActions
from math import sqrt

nltk.download('stopwords')
custom_stopwords = {'media','omitted','message','deleted','edited','https','com'}

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

def get_ratioed(total_messages: dict[str,int], count: dict[str,int]):
    for user, total_message_count in total_messages.items():
        count[user] = [count.get(user), f"1 in {round(total_message_count/count.get(user)) if total_message_count*count.get(user) != 0 else 0}"]

    return count

def get_messages_count(user_messages: dict, check_strings: str | list[str] = None) -> dict[str, int]:
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
    """
    Uses regex to identify text-based emoticons
    """
    emoticons_pattern = re.compile(
    r"""(?<!\S)         # no non-space before
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
    emoji_counter, emoticon_counter, emojis_emoticons_used = {}, {}, {}
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
        emoji_counter[user] = emoji_count
        emoticon_counter[user] = emoticon_count
        emojis_emoticons_used[user] = [dict(emoji_freq.most_common()), dict(emoticon_freq.most_common())]

    return emoji_counter, emoticon_counter, emojis_emoticons_used

def classify_url(raw_url: str) -> str:
    """
    Maps URL to avoid repeated entries
    """

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
    """
    Counts the urls and also returns all the links sent by a user
    """
    url_pattern = re.compile(r"https?://\S+")
    url_count, detailed_url_count = {}, {}

    for user, messages in user_messages.items():
        urls = []
        count = defaultdict(int)
        total_count = 0
        for msg in messages:
            found_urls = url_pattern.findall(msg)
            for raw_url in found_urls:
                platform = classify_url(raw_url)
                urls.append(raw_url)
                count[platform] += 1
                total_count += 1
        sorted_count = dict(sorted(count.items(), key=lambda x: x[1], reverse=True))
        url_count[user] = total_count
        detailed_url_count[user] = [sorted_count, urls]

    return url_count, detailed_url_count

def get_word_char_stats(user_messages: dict):
    """
    Get number of words and characters sent by a user
    """
    wc_stats = {}
    for user, messages in user_messages.items():
        m_count, w_count, c_count = 0,0,0
        words, chars = [], []
        for msg in messages:
            w_count += len(msg.split())
            c_count += len(msg)
            words.append(len(msg.split()))
            chars.append(len(msg))
            m_count+=1
        w_median = statistics.median(words)
        w_mean = int(statistics.mean(words))
        w_mode = statistics.mode(words)
        c_median = statistics.median(chars)
        c_mean = int(statistics.mean(chars))
        c_mode = statistics.mode(chars)
        wc_stats[user] = {
            "messages": m_count,
            "words": w_count,
            "characters": c_count,
            "characters/word": round(c_count/w_count,2) if w_count != 0 else 0,
            "words/message": round(w_count/m_count,2) if m_count != 0 else 0,
            "characters/message": round(c_count/m_count,2) if m_count != 0 else 0,
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
) -> dict:
    """

    :param date_times: Takes in a list of datetime objects
    :param messages: List of all the user messages
    :param users: List of users in the chat
    :param min_convo_time: Parameter for setting the minimum threshold
    :param min_convo_length: Parameter for setting the maximum threshold
    :param top_n: Parameter for returning the top_n number of convos
    :return: A dictionary with:
            Gap threshold (in seconds),
            Longest convo,
            Convo with the most no.of messages exchanged,
            Convos ordered by messages per minute,
            Convos ordered by messages per minute times unique participants per minute
    """

    if len(date_times) != len(messages) != len(users):
        return {"Error": "Length of dates, messages and users list do not match!"}
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
        "gap threshold in seconds": gap_thresh.total_seconds(),
        "Longest conversation": longest_conversation,
        "Most messages conversation": most_messages_conversation,
        f"Top {top_n} by messages / min":
            sorted(all_conversations, key=lambda x: x["messages_per_min"], reverse=True)[:top_n],
        f"Top {top_n} by messages / min * unique participants / min":
            sorted(all_conversations,
                   key=lambda x: x["messages_per_min"] * x["unique_participants_per_min"], reverse=True)[:top_n],
    }

def get_longest_streak(dates: list[datetime.date]):
    """
    Gets the longest streak in days
    """
    dates = sorted(set(dates))
    streak = count = 1
    streak_start = streak_end = dates[0]
    temp_start = dates[0]
    for i in range(len(dates) - 1):
        if dates[i + 1] - dates[i] <= timedelta(days=1):
            count += 1
            if count > streak:
                streak = count
                streak_start = temp_start
                streak_end = dates[i + 1]
        else:
            count = 1
            temp_start = dates[i + 1]

    return {
        "Streak start": streak_start,
        "Streak end": streak_end,
        "Streak in days": streak
    }

def get_day_wise_freq(dates: list[datetime.date]) -> dict[str:int]:
    day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    day_counter = {"Monday":0, "Tuesday":0, "Wednesday":0, "Thursday":0, "Friday":0, "Saturday":0, "Sunday":0}
    for date in dates:
        day_counter[day_names[date.weekday()]] += 1

    return day_counter

def get_time_wise_freq(times: list[datetime.time]) -> dict[datetime.time:int]:
    time_counter = Counter()
    for time in times:
        time_counter[time.hour] += 1

    return dict(time_counter)

def get_date_wise_freq(dates: list[datetime.date], top_n:int = None) -> dict[datetime.date:int]:
    date_counter = Counter()
    for date in dates:
        date_counter[date] += 1

    if top_n is None: return dict(date_counter)
    return dict(date_counter.most_common(top_n))

def get_detailed_timeseries(dates: list[datetime.date], user_messages:dict) -> dict[datetime.date:list[int,int]]:
    counter = defaultdict(lambda: defaultdict(lambda: {"messages": 0,
                                                       "words": 0,
                                                       "characters": 0,
                                                       "characters/word": 0,
                                                       "words/message": 0,
                                                       "characters/message": 0,
                                                       "deleted": 0,
                                                       "edited": 0,
                                                       "media": 0,
                                                       "links": 0,
                                                       "emojis": 0,
                                                       "emoticons": 0}))

    for user, dict_ in user_messages.items():
        for date, messages_ in dict_.items():

            stats = get_word_char_stats({user: messages_})
            counter[date][user]["messages"] += stats[user]["messages"]
            counter[date][user]["words"] += stats[user]["words"]
            counter[date][user]["characters"] += stats[user]["characters"]
            counter[date][user]["characters/word"] += stats[user]["characters/word"]
            counter[date][user]["words/message"] += stats[user]["words/message"]
            counter[date][user]["characters/message"] += stats[user]["characters/message"]
            counter[date][user]["deleted"] += sum(get_messages_deleted_count({user: messages_}).values())
            counter[date][user]["edited"] += sum(get_messages_edited_count({user: messages_}).values())
            counter[date][user]["media"] += sum(get_media_sent_count({user: messages_}).values())
            counter[date][user]["links"] += sum(get_links({user: messages_})[0].values())
            emojis, emoticons, _ = get_emoji_emoticon_count({user: messages_})
            counter[date][user]["emojis"] += sum(emojis.values())
            counter[date][user]["emoticons"] += sum(emoticons.values())

        if user in list not in dict:

    return counter

def get_user_reply_map(users_wrt_messages: list[str]) -> dict[str, dict[str, int]]:
    reply_map = defaultdict(lambda: defaultdict(int))

    for i in range(1, len(users_wrt_messages)):
        prev_user = users_wrt_messages[i - 1]
        cur_user = users_wrt_messages[i]
        if prev_user != cur_user:
            # Avoid elf replies
            reply_map[cur_user][prev_user] += 1

    return {user: dict(replies) for user, replies in reply_map.items()}

def normalise_reply_map(
        reply_map: dict[str, dict[str, int]],
        total_messages: dict[str, int]
):
    interaction_strength = defaultdict(dict)

    # Symmetric interaction strength - how strong mutual communication is
    users = set(reply_map.keys()) | set(total_messages.keys())
    for a in users:
        for b in users:
            if a == b:
                continue
            a_b = reply_map.get(a, {}).get(b, 0)
            b_a = reply_map.get(b, {}).get(a, 0)
            total_a = total_messages.get(a, 1)
            total_b = total_messages.get(b, 1)
            score = (a_b + b_a) / sqrt(total_a * total_b)
            if score > 0:
                interaction_strength[a][b] = round(score, 3)

    return {
        "raw": reply_map,
        "interaction_strength": dict(interaction_strength),
    }


# All functions below are related to milestone function
def _to_datetime(date: datetime.date, time: datetime.time = time(0,0,0)) -> datetime:
    """
    Combines date and time
    """
    return datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M:%S")

def get_group_creation(system_messages: list[dict]):
    for msg in system_messages:
            if msg["action"] == SysMsgActions.CreateGroup:
                return msg

def get_nth_message(user_messages:list[dict], n: int):
    for i in range(1,len(user_messages)):
        if i==n:
            return user_messages[n]

def get_user_first_message(user_messages:list[dict], user: str):
    for msg in user_messages:
        if msg["sender"] is user:
            return msg

def get_user_joins(user_messages:list[dict], system_messages: list[dict], user_list: list[str]):
    user_joins = {}
    mod_user_list = user_list.copy()
    grp_created = get_group_creation(system_messages)
    for msg in system_messages:
        if msg["action"] == SysMsgActions.AddUser:
            if msg["added"] in mod_user_list:
                user_joins.update({f"{msg["added"]}":_to_datetime(msg["date"], msg["time"])})
                mod_user_list.remove(msg["added"])
        if msg["action"] == SysMsgActions.CreateGroup:
            # For the user who created the group
            user_joins.update({f"{msg["author"]}": _to_datetime(grp_created["date"], grp_created["time"])})
            mod_user_list.remove(msg["author"])


    for user in user_list:
        if user_joins.get(user) and hasattr(user_joins[user], "date"):
            # For those that joined before the group was created, set it as when the group was created
            if user_joins[user].date() > get_user_first_message(user_messages, user)["date"]:
                user_joins[user] = _to_datetime(grp_created["date"], grp_created["time"])
        elif user not in user_joins.keys():
            # For the user who uploaded the log, since they will be addressed as "You" by the system
            user_joins[user] = _to_datetime(grp_created["date"], grp_created["time"])

    user_joins = ((b,f"{a} has joined the chat") for a,b in user_joins.items())
    return user_joins

def get_milestones(
        user_messages:list[dict],
        system_messages:list[dict],
        user_list: list[str],
        dates: list[datetime.date],
        top_convos: dict,
        streak: dict,
        is_group: bool
) -> list[tuple[str,str]]:
    """
    Covers these milestones:
    - Group creation
    - When each member joined
    - Group name changes
    - First message sent by each user
    - Every 100th, 1000th, 10000th... message
    - The day when most messages exchanged
    - Longest convo in minutes
    - Most messages sent in a convo
    - Streak start and end

    Sorts them by time and returns the datetime and the reason for milestone as tuple
    """
    grp_milestones = []
    chat_milestones = []

    if is_group:
        # Group creation
        _ = get_group_creation(system_messages)
        grp_milestones.append((_to_datetime(_["date"], _["time"]), f"The group {_["name"]} was created by {_["author"]}"))

        #When each member joined
        for _ in get_user_joins(user_messages, system_messages, user_list): grp_milestones.append(_)

        # Group name changes
        for _ in [msg for msg in system_messages if msg["action"] == SysMsgActions.ChangeGrpName or msg["action"] == SysMsgActions.ChangeGrpName]:
            grp_milestones.append((_to_datetime(_["date"], _["time"]), f"The group name was changed from {_["name_change"]} by {_["author"]}"))

    # First message sent by each user
    for user in user_list:
        _ = get_user_first_message(user_messages, user)
        date, time, sender, message = _["date"], _["time"], _["sender"], _["message"]
        chat_milestones.append((_to_datetime(date, time), f"The 1st message sent by {sender} : {message}"))

    # Add every 100th, 1000th, 10000th... message to the milestone
    i=99
    while i <= len(user_messages):
        _ = get_nth_message(user_messages, i)
        chat_milestones.append((_to_datetime(_["date"], _["time"]), f"The {i}th message was sent by {_["sender"]} : {_["message"]}"))
        if i % 10 == 1:
            i-=1
            i*=10
            i-=1
        else: i+=1

    # Day with the most messages is added
    most_active_day, count = next(iter(get_date_wise_freq(dates, 1).items()))
    chat_milestones.append((_to_datetime(most_active_day), f"{count} messages were exchanged in a single day, the highest in this chat's history!"))

    # Longest convo
    longest_convo = top_convos["Longest conversation"]
    chat_milestones.append((longest_convo["start"],
                            f"Had the longest conversation that lasted for {longest_convo["duration_min"]} minutes and "
                            f"exchanged over {longest_convo["messages"]} messages!"))

    # Most messages sent in a convo
    most_messages_convo = top_convos["Most messages conversation"]
    # If the longest convo is same as most messages sent then skip
    if longest_convo["start"] != most_messages_convo["start"]:
        chat_milestones.append((most_messages_convo["start"],
                            f"Had a conversation where you exchanged over {most_messages_convo["messages"]} messages "
                            f"that lasted {most_messages_convo["duration_min"]} minutes."))

    # Longest streak
    chat_milestones.append((_to_datetime(streak["Streak start"]),
                            f"From today for the next {streak["Streak in days"]} days, at least a single message is exchanged!"))
    chat_milestones.append((_to_datetime(streak["Streak end"]), f"The {streak["Streak in days"]} day streak ended today."))

    for _ in grp_milestones:
        chat_milestones.append(_)

    chat_milestones = sorted(chat_milestones, key = lambda x: x[0])

    return chat_milestones


