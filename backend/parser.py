from datetime import datetime
import re

class Parser:
    def __init__(self, chat_text: str):
        self.chat_text = chat_text
        self.messages = self._parse_to_list()

    def _parse_to_list(self) -> list[dict]:
        """
        Matches the pattern and returns a list of dicts
        """
        date = r"(\d{2})/(\d{2})/(\d{4})"
        time = r"(\d{2}):(\d{2})"
        name = r"([^:]+)"
        message = r"(.*?)(?=\n\d{2}/\d{2}/\d{4},\s+\d{2}:\d{2}\s+-|$)"
        # .*? -> Non-greedy match
        # ?= -> Lookahead

        pattern = re.compile(
            rf"{date},\s+{time}\s+-\s+{name}:\s+{message}",
            re.DOTALL
        )
        messages = pattern.findall(self.chat_text)

        return [
            {
                "date": f"{day}/{month}/{year}",
                "time": f"{hour}:{minute}",
                "sender": sender.strip(),
                "message": content.strip()
            }
            for day, month, year, hour, minute, sender, content in messages
        ]

    def get_dates(self) -> list[datetime.date]:
        """
        Get formated dates for all the messages
        """
        return [
            datetime.strptime(msg["date"], "%d/%m/%Y").date()
            for msg in self.messages
        ]

    def get_time(self) -> list[datetime.time]:
        """
        Get formated time for all the messages
        """
        return [
            datetime.strptime(msg["time"], "%H:%M").time()
            for msg in self.messages
        ]

    def get_users_wrt_messages(self) -> list[str]:
        """
        Gets the usernames with respect to each message
        """
        return list(msg["sender"] for msg in self.messages)

    def get_users(self) -> list[str]:
        """
        Gets the usernames of everyone in thr group
        Note: Does not work if they have never sent a message
        """
        return list(set(msg["sender"] for msg in self.messages))

    def get_messages_by_user(self, user:str = None) -> list[str]:
        """
        Get messages sent by a user
        """
        if user is None:
            return [msg["message"] for msg in self.messages]
        return [msg["message"] for msg in self.messages if msg["sender"] == user]

    def get_date_time_by_user(self, user:str = None) -> list[datetime]:
        """
        Get dates and times of messages sent by a user
        """
        if user is None:
            return [
                datetime.strptime(f"{msg["date"]} {msg["time"]}", "%d/%m/%Y %H:%M")
                for msg in self.messages
            ]
        return [
            datetime.strptime(f"{msg["date"]} {msg["time"]}", "%d/%m/%Y %H:%M")
            for msg in self.messages if msg["sender"] == user
        ]

    def get_date_by_user(self, user:str = None) -> list[datetime.time]:
        """
        Get dates of messages sent by a user
        """
        if user is None:
            return [
                datetime.strptime(msg["date"], "%d/%m/%Y").date()
                for msg in self.messages
            ]
        return [
            datetime.strptime(msg["date"], "%d/%m/%Y").date()
            for msg in self.messages if msg["sender"] == user
        ]

    def get_time_by_user(self, user:str = None) -> list[datetime.time]:
        """
        Get time of messages sent by a user
        """
        if user is None:
            return [
                datetime.strptime(msg["time"], "%H:%M").time()
                for msg in self.messages
            ]
        return [
            datetime.strptime(msg["time"], "%H:%M").time()
            for msg in self.messages if msg["sender"] == user
        ]
