import json
from typing import List
import uuid
import re

from bibleduel.models.player import Player


class User:

    def __init__(self, _id, username, password, friends, score, role):
        self._id = _id if _id is not None else uuid.uuid4().hex
        self.username = username
        self.friends = friends
        self.score = score
        self.role = role
        self.password = password
        self.salt = None

    @staticmethod
    def create_new_user(username: str, password: str, salt: str):
        _id = uuid.uuid4().hex
        friends: List[Player] = []
        score = 0
        role = "user"
        new_user = User(_id, username, password, friends, score, role)
        new_user.salt = salt
        return new_user

    @property
    def id(self):
        return self._id

    def toJSON(self):
        return {
            '_id': self._id,
            'username': self.username,
            "password": self.password,
            "salt": self.salt,
            'friends': [friend.toJSON() for friend in self.friends],
            'score': self.score,
            'role': self.role
        }

    def to_transmit_json(self):
        return {
            "_id": self._id,
            "username": self.username,
            "friends": self.friends,
            "score": self.score,
            "role": self.role
        }

    @staticmethod
    def fromJSON(json_obj):
        return User(
            json_obj['_id'],
            json_obj['username'],
            json_obj['password'],
            [Player.fromJSON(friend).to_dict() for friend in json_obj['friends']] if json_obj['friends'] else [],
            json_obj['score'],
            json_obj['role']
        )

    def validate(self) -> (bool, str):
        if not (self.username and 4 <= len(self.username) <= 20 and re.match("^[a-zA-Z0-9]+$", self.username)):
            return True, "valid"

        if not (self.password and 4 <= len(self.password) <= 20 and re.match("^[a-zA-Z0-9]+$", self.password)):
            return True, "valid"

        return True, "valid"
