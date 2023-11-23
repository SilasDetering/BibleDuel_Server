import json


class Question:
    def __init__(self, id: int, title: str, category: str, options: list, answer: str):
        self.id = id
        self.title = title
        self.category = category
        self.options = options
        self.answer = answer

    def to_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "category": self.category,
            "options": self.options,
            "answer": self.answer,
        }

    def to_json_string(self):
        return json.dumps(self.to_json())
