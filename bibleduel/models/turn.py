import json

from bibleduel.models.category import Category
from bibleduel.models.question import Question


class Turn:
    def __init__(self, questions, category, player_answers=None):
        self.questions = questions
        self.category = category
        self.playerAnswers = player_answers if player_answers is not None else {}

    def toJSON(self):
        return {
            "questions": [question.toJSON() for question in self.questions],
            "category": self.category.toJSON(),
            "playerAnswers": self.playerAnswers
        }

    @staticmethod
    def fromJSON(json_str):
        parsed_json = json.loads(json_str)

        questions = [Question.fromJSON(json.dumps(question)) for question in parsed_json["questions"]]
        category = Category.fromJSON(json.dumps(parsed_json["category"]))

        return Turn(questions, category, parsed_json.get("playerAnswers", {}))
