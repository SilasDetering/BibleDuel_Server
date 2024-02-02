import json


class Player:
    def __init__(self, _id, username, score):
        self._id = _id
        self.username = username
        self.score = score

    def toJSON(self):
        return {
            "_id": self._id,
            "username": self.username,
            "score": self.score,
        }

    @staticmethod
    def fromJSON(data):

        if isinstance(data, str):
            parsed_json = json.loads(data)
        else:
            parsed_json = data

        return Player(
            parsed_json["_id"],
            parsed_json["username"],
            parsed_json["score"],
        )

    def to_dict(self):
        return {
            "_id": self._id,
            "username": self.username,
            "score": self.score,
        }

    @staticmethod
    def user_to_player(user):
        return Player(
            user["_id"],
            user["username"],
            user["score"],
        )

    @staticmethod
    def user_to_player_dict(user):
        return {
            "_id": user["_id"],
            "username": user["username"],
            "score": user["score"],
        }
