import json


class Player:
    def __init__(self, username: str, icon: any, score: int, ratio: float):
        self.username = username
        self.icon = icon
        self.score = score
        self.ratio = ratio

    def to_json(self):
        return {
            "username": self.username,
            "icon": self.icon,
            "score": self.score,
            "ratio": self.ratio
        }

    def to_json_string(self):
        return json.dumps(self.to_json())

    @staticmethod
    def from_json(json_string: str):
        parsed_json = json.loads(json_string)
        return Player(
            parsed_json["username"],
            parsed_json["icon"],
            parsed_json["score"],
            parsed_json["ratio"]
        )
