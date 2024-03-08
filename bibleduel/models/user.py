import uuid
import re


class User:

    def __init__(self, _id, username, password, friends, score, role, salt=None):
        self._id = _id if _id is not None else uuid.uuid4().hex
        self.username = username
        self.friends = friends if friends is not None else {}
        self.score = int(score) if score is not None else 0
        self.role = role if role is not None else "user"
        self.password = password
        self.salt = salt

    def to_dict(self):
        return {
            '_id': self._id,
            'username': self.username,
            "password": self.password,
            "salt": self.salt,
            'friends': self.friends,
            'score': self.score,
            'role': self.role
        }

    def to_transmit_dict(self):
        return {
            "_id": self._id,
            "username": self.username,
            "score": self.score,
            "role": self.role
        }

    @staticmethod
    def fromJSON(json_obj):
        user = User(
            json_obj['_id'],
            json_obj['username'],
            json_obj['password'],
            json_obj['friends'],
            json_obj['score'],
            json_obj['role'],
            json_obj['salt']
        )
        return user

    def validate_password(self) -> None or str:
        if not (self.password and 4 <= len(self.password) <= 20
                and re.match("^[a-zA-Z0-9!@#$%^&*()_+]+$", self.password)):
            return "Ungültiges Passwort"

        return None

    def validate_username(self) -> None or str:
        if not (self.username and 4 <= len(self.username) <= 20 and re.match("^[a-zA-Z0-9]+$", self.username)):
            return "Ungültiger Benutzername"

        return None
