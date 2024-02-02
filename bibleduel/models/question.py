import json
import uuid
from bibleduel.models.category import Category


class Question:
    def __init__(self, _id, title, category, options, answer, source):
        self._id = _id if _id is not None else uuid.uuid4().hex
        self.title = title
        self.category = category
        self.options = options
        self.answer = answer
        self.source = source

    @staticmethod
    def fromJSON(json_str):
        parsed_json = json.loads(json_str)
        return Question(
            parsed_json['_id'],
            parsed_json['title'],
            parsed_json['category'],
            parsed_json['options'],
            parsed_json['answer'],
            parsed_json['source']
        )

    def to_dict(self):
        return {
            '_id': self._id,
            'title': self.title,
            'category': self.category,
            'options': self.options,
            'answer': self.answer,
            'source': self.source
        }
