from datetime import datetime
import re
from constants import ACTIONS

class Parser:
    def __init__(self, chat_text: str):
        self.chat_text = chat_text
        self.user_messages, self.system_messages = self._parse_to_list()

    def _parse_to_list(self) -> (list[dict], list[dict]):
        """
        Split the raw chat into timestamped entries, then classify each entry
        as a user message (has 'Sender: ') or a system message (no sender).
        Returns (user_messages, system_messages).
        """

        #split on timestamp boundaries (keep each chunk starting with a timestamp)
        # (?m) => multiline so ^ matches line-start
        # (?=...) => lookahead so split keeps the boundary as part of the chunk
        entry_split_re = re.compile(r'(?m)(?=^\d{2}/\d{2}/\d{4},\s+\d{2}:\d{2}\s+-\s)')
        chunks = entry_split_re.split(self.chat_text.strip())

        #regex to parse an entry into date/time and optional sender + the rest as content
        # - date/time are captured
        # - (?:(?P<sender>[^:]+):\s*)? matches "Sender: " optionally (if present it's a user msg)
        # - (?P<content>.*) with DOTALL captures all following lines (multiline message)
        entry_re = re.compile(
            r'^\s*'
            r'(?P<date>\d{2}/\d{2}/\d{4}),\s*'
            r'(?P<time>\d{2}:\d{2})\s*-\s*'
            r'(?:(?P<sender>[^:]+):\s*)?'
            r'(?P<content>.*)$',
            re.DOTALL | re.MULTILINE
        )

        user_messages = []
        system_messages = []

        for chunk in chunks:
            if not chunk.strip():
                continue
            m = entry_re.match(chunk)
            if not m:
                #chunk didn't match the expected entry format; treat as system text
                system_messages.append({
                    "date": None,
                    "time": None,
                    "system_message": chunk.strip(),
                    "author": None,
                    "action": None
                })
                continue

            date = datetime.strptime(m.group('date'), "%d/%m/%Y").date()
            time = datetime.strptime(m.group('time'), "%H:%M").time()
            sender = m.group('sender')
            content = m.group('content').rstrip()

            if sender:
                user_messages.append({
                    "date": date,
                    "time": time,
                    "sender": sender.strip(),
                    "message": content.strip()
                })
            else:
                system_messages.append({
                    "date": date,
                    "time": time,
                    "system_message": content.strip(),
                    "author": None,
                    "action": None
                })

        for msg in system_messages:
            for action, handler in ACTIONS.items():
                if action in msg["system_message"]:
                    parts = msg["system_message"].split(action)
                    msg.update({"action": action})
                    msg.update(handler(parts))

        return user_messages, system_messages

    def is_group(self) -> bool:
        """
        Checks if the chat uploaded is that of a group or between two ppl
        """
        if len(self.get_users()) > 2: return True
        return False

    def get_dates(self) -> list[datetime.date]:
        """
        Get formated dates for all the messages
        """
        return [msg["date"] for msg in self.user_messages]

    def get_time(self) -> list[datetime.time]:
        """
        Get formated time for all the messages
        """
        return [msg["time"] for msg in self.user_messages]

    def get_users_wrt_messages(self) -> list[str]:
        """
        Gets the usernames with respect to each message
        """
        return list(msg["sender"] for msg in self.user_messages if msg["sender"] != "Meta AI")

    def get_users(self) -> list[str]:
        """
        Gets the usernames of everyone in thr group
        Note: Does not work if they have never sent a message
        """
        return list(set(msg["sender"] for msg in self.user_messages if msg["sender"] != "Meta AI"))

    def get_messages_by_user(self, user:str = None) -> list[str]:
        """
        Get messages sent by a user
        """
        if user is None:
            return [msg["message"] for msg in self.user_messages]
        return [msg["message"] for msg in self.user_messages if msg["sender"] == user]

    def get_date_time_by_user(self, user:str = None) -> list[datetime]:
        """
        Get dates and times of messages sent by a user
        """
        if user is None:
            return [
                datetime.strptime(f"{msg["date"]} {msg["time"]}", "%Y-%m-%d %H:%M:%S")
                for msg in self.user_messages
            ]
        return [
            datetime.strptime(f"{msg["date"]} {msg["time"]}", "%d/%m/%Y %H:%M")
            for msg in self.user_messages if msg["sender"] == user
        ]

    def get_date_by_user(self, user:str = None) -> list[datetime.time]:
        """
        Get dates of messages sent by a user
        """
        if user is None:
            return [msg["date"] for msg in self.user_messages]
        return [msg["date"] for msg in self.user_messages if msg["sender"] == user]

    def get_time_by_user(self, user:str = None) -> list[datetime.time]:
        """
        Get time of messages sent by a user
        """
        if user is None:
            return [msg["time"] for msg in self.user_messages]
        return [msg["time"] for msg in self.user_messages if msg["sender"] == user]
