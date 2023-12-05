import json
import uuid


class Question:
    def __init__(self, title: str, category: str, options: list, answer: str):
        self._id = uuid.uuid4().hex
        self.title = title
        self.category = category
        self.options = options
        self.answer = answer

    def __tojson__(self):
        return {
            "id": self._id,
            "title": self.title,
            "category": self.category,
            "options": self.options,
            "answer": self.answer,
        }