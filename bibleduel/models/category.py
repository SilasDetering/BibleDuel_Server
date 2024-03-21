import json


class Category:
    def __init__(self, _id, title, subtitle, author, color, timelimit):
        self._id = _id
        self.title = title
        self.subtitle = subtitle
        self.author = author
        self.color = color
        self.timelimit = int(timelimit) or 20

    @staticmethod
    def fromJSON(json_str):
        parsed_json = json.loads(json_str)
        return Category(
            parsed_json['_id'],
            parsed_json['title'],
            parsed_json['subtitle'],
            parsed_json['author'],
            parsed_json['color'],
            parsed_json['timelimit']
        )

    def to_dict(self):
        return {
            '_id': self._id,
            'title': self.title,
            'subtitle': self.subtitle,
            'author': self.author,
            'color': self.color,
            'timelimit': self.timelimit,
        }
