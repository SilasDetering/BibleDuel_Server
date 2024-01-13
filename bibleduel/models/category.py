import json


class Category:
    def __init__(self, title, color):
        self.title = title
        self.color = color

    @staticmethod
    def _fromJSON(json_str):
        parsed_json = json.loads(json_str)
        return Category(parsed_json['title'], parsed_json['color'])

    def _toJSON(self):
        return json.dumps({'title': self.title, 'color': self.color})
