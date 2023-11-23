from typing import List


class User:
    def __init__(self, username: str, icon: any):
        self.username = username
        self.icon = icon
        self.friends = {}
        self.score = 0
        self.role = "user"

    def get_friends(self) -> List[dict]:
        return list(self.friends.values())

    def add_friend(self, username: str):
        self.friends[username] = [0, 0, 0]

    def remove_friend(self, username: str):
        if username in self.friends:
            del self.friends[username]
