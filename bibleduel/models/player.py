import json
import uuid


class Player:
    def __init__(self, _id, username, score, ratio):
        self._id = _id
        self.username = username
        self.score = score
        self.ratio = ratio

    def _toJSON(self):
        return {
            "_id": self._id,
            "username": self.username,
            "score": self.score,
            "ratio": self.ratio
        }

    def to_json_string(self):
        return json.dumps(self._toJSON())

    @staticmethod
    def _fromJSON(json_string: str):
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
