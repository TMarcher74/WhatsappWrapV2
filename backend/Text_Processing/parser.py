from collections import defaultdict
from datetime import datetime
import re
from backend.Util.constants import ACTIONS

class Parser:
    def __init__(self, chat_text: str):
        self.chat_text = chat_text
        self.user_messages, self.system_messages = self._parse_to_list()

    def _parse_to_list(self) -> tuple[list[dict], list[dict]]:
        """
        Split the raw chat into timestamped entries, then classify each entry
        as a user message (has 'Sender: ') or a system message (no sender).
        Returns (user_messages, system_messages).
        """

        #split on timestamp boundaries (keep each chunk starting with a timestamp)
        # (?m) => multiline so ^ matches line-start
        # (?=...) => lookahead so split keeps the boundary as part of the chunk
        entry_split_re = re.compile(
            r'(?m)(?=^\d{1,2}[-/.]\d{1,2}[-/.]\d{2,4}[,\s]+\d{1,2}[:.]\d{2}\s*(?:[ap]m)?\s*-\s*)',
            re.IGNORECASE
        )
        chunks = entry_split_re.split(self.chat_text.strip())

        #regex to capture an entry of date/time and optional sender + the rest as content
        entry_re = re.compile(
            r'^\s*'
            r'(?P<date>\d{1,2}[-/.]\d{1,2}[-/.]\d{2,4})'
            r'[,\s]+'
            r'(?P<time>\d{1,2}[:.]\d{2}\s*(?:[ap]m)?)'
            r'\s*-\s*'
            r'(?:(?P<sender>[^:]+):\s*)?'
            r'(?P<content>.*)$',
            re.DOTALL | re.MULTILINE | re.IGNORECASE
        )

        user_messages = []
        system_messages = []

        date_format, time_format = self.sniff_date_time_format()

        for chunk in chunks:
            if not chunk.strip():
                continue
            m = entry_re.match(chunk)
            if not m:
                #chunk didn't match the expected entry format, treat as system text
                system_messages.append({
                    "date": None,
                    "time": None,
                    "system_message": chunk.strip(),
                    "author": None,
                    "action": None
                })
                continue

            def parse_with_strptime(date_str, time_str, date_format, time_format):
                # format codes to strptime format strings
                date_fmt_map = {'EU': '%d/%m/%Y', 'US': '%m/%d/%y'}
                time_fmt_map = {'24H': '%H:%M', '12H': '%I:%M %p'}

                #Combine and parse
                fmt_string = f'{date_fmt_map[date_format]} {time_fmt_map[time_format]}'
                return datetime.strptime(f'{date_str.strip()} {time_str.strip()}', fmt_string)

            date_time = parse_with_strptime(m.group('date'), m.group('time'), date_format, time_format)
            date = date_time.date()
            time = date_time.time()
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

    def sniff_date_time_format(self) -> tuple[str, str]:
        """
        Sniff the date/time format from the first valid timestamp in the chat.
        Returns (date_format, time_format)
        """
        lines = self.chat_text.strip().split('\n')

        # Look for the first line with a timestamp
        timestamp_re = re.compile(
            r'^\s*(\d{1,2}[-/.]\d{1,2}[-/.]\d{2,4})[,\s]+(\d{1,2}[:.]\d{2}\s*(?:[ap]m)?)',
            re.IGNORECASE
        )

        # Default
        date_format = 'EU'
        time_format = '24H'

        for line in lines:
            match = timestamp_re.match(line)
            if match:
                date_str, time_str = match.groups()

                # Determine time format
                time_format = '12H' if ('am' in time_str.lower() or 'pm' in time_str.lower()) else '24H'

                # Determine date format
                # Normalize and split
                normalized_date = re.sub(r'[-./]', '/', date_str)
                parts = normalized_date.split('/')

                if len(parts) == 3:
                    first, second, _ = parts
                    first_int = int(first) if first.isdigit() else 0
                    second_int = int(second) if second.isdigit() else 0

                    if first_int > 12:
                        date_format = 'EU'  # First part > 12 must be day
                        break
                    elif second_int > 12:
                        date_format = 'US'  # Second part > 12 must be month
                        break
                    else:
                        # Ambiguous
                        continue

        return date_format, time_format

    def is_group(self) -> bool:
        """
        Checks if the chat uploaded is that of a group or between two ppl
        """
        if len(self.get_users()) > 2: return True
        return False

    def get_users_wrt_messages(self) -> list[str]:
        """
        Gets the usernames with respect to each message
        """
        return list(msg["sender"] for msg in self.user_messages)

    def get_users(self) -> list[str]:
        """
        Gets the usernames of everyone in thr group
        Note: Does not work if they have never sent a message
        """
        return list(set(msg["sender"] for msg in self.user_messages))

    def get_messages_by_user(self, user:str = None) -> list[str]:
        """
        Get messages sent by a user
        """
        if user is None:
            return [msg["message"] for msg in self.user_messages]
        return [msg["message"] for msg in self.user_messages if msg["sender"] == user]

    def get_date_and_messages_by_user(self, user:str = None) -> dict[datetime, list[str]]:
        """
        Get messages sent by a user
        """
        grouped = defaultdict(list)
        if user is None:
            for msg in self.user_messages:
                grouped[msg["date"]].append(msg["message"])
            return dict(grouped)
        for msg in self.user_messages:
            if msg["sender"] == user:
                grouped[msg["date"]].append(msg["message"])
        return dict(grouped)

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

    def get_date_by_user(self, user:str = None) -> list[datetime]:
        """
        Get dates of messages sent by a user
        """
        if user is None:
            return [msg["date"] for msg in self.user_messages]
        return [msg["date"] for msg in self.user_messages if msg["sender"] == user]

    def get_time_by_user(self, user:str = None) -> list[datetime]:
        """
        Get time of messages sent by a user
        """
        if user is None:
            return [msg["time"] for msg in self.user_messages]
        return [msg["time"] for msg in self.user_messages if msg["sender"] == user]
