import json
from typing import List
import uuid
import re

from bibleduel.models.player import Player


class User:
    def __init__(self, username: str, password: str, salt: str):
        self._id = uuid.uuid4().hex
        self.username = username
        self.password = password
        self.salt = salt
        self.friends: List[Player] = []
        self.score = 0
        self.role = "user"

    @property
    def id(self):
        return self._id

    @staticmethod
    def from_json(json_data):
        user = User(username=json_data["username"], password=json_data["password"], salt=json_data["salt"])
        user._id = json_data["_id"]
        user.friends = json_data["friends"]
        user.score = json_data["score"]
        user.role = json_data["role"]

        return user

    def to_json(self):
        return {
            "_id": self._id,
            "username": self.username,
            "password": self.password,
            "salt": self.salt,
            "friends": self.friends,
            "score": self.score,
            "role": self.role
        }

    def to_transmit_json(self):
        return {
            "_id": self._id,
            "username": self.username,
            "friends": self.friends,
            "score": self.score,
            "role": self.role
        }

    def validate(self) -> (bool, str):
        if not (self.username and 4 <= len(self.username) <= 20 and re.match("^[a-zA-Z0-9]+$", self.username)):
            return True, "valid"

        if not (self.password and 4 <= len(self.password) <= 20 and re.match("^[a-zA-Z0-9]+$", self.password)):
            return True, "valid"

        return True, "valid"
