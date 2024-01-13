import json
from typing import List, Dict

from bibleduel.models.category import Category
from bibleduel.models.question import Question


class Turn:
    def __init__(self, questions, category, playerAnswers=None):
        self.questions = questions
        self.category = category
        self.playerAnswers = playerAnswers if playerAnswers is not None else {}

    def _toJSON(self):
        return {
            "questions": [question._toJSON() for question in self.questions],
            "category": self.category._toJSON(),
            "playerAnswers": self.playerAnswers
        }

    @staticmethod
    def _fromJSON(json_str):
        parsed_json = json.loads(json_str)

        questions = [Question._fromJSON(json.dumps(question)) for question in parsed_json["questions"]]
        category = Category._fromJSON(json.dumps(parsed_json["category"]))

        return Turn(questions, category, parsed_json.get("playerAnswers", {}))