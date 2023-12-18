import json
import uuid


class Player:
    def __init__(self, _id: uuid, username: str, score: int, ratio: float):
        self._id = _id
        self.username = username
        self.score = score
        self.ratio = ratio

    def to_json(self):
        return {
            "_id": self._id,
            "username": self.username,
            "score": self.score,
            "ratio": self.ratio
        }

    def to_json_string(self):
        return json.dumps(self.to_json())

    @staticmethod
    def from_json(json_string: str):
        parsed_json = json.loads(json_string)
        return Player(
            parsed_json["_id"],
            parsed_json["username"],
            parsed_json["score"],
            parsed_json["ratio"]
        )

    @staticmethod
    def user_to_player_json(user):
        return {
            "_id": user["_id"],
            "username": user["username"],
            "score": user["score"],
            "ratio": [0, 0, 0]
        }

    @property
    def id(self):
        return self._id
