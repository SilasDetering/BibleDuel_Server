import json


class Credentials:
    def __init__(self):
        self.username = None
        self.password = None
        self.icon = None

    def to_json(self):
        return {
            "username": self.username,
            "password": self.password,
            "icon": self.icon
        }

    def to_json_string(self):
        return json.dumps(self.to_json())

    @staticmethod
    def from_json(json_string: str):
        parsed_json = json.loads(json_string)
        credentials = Credentials()
        credentials.username = parsed_json.get("username")
        credentials.password = parsed_json.get("password")
        credentials.icon = parsed_json.get("icon")
        return credentials
