import json
from bibleduel.models.category import Category
from bibleduel.models.question import Question
from collections import defaultdict


class Turn:
    def __init__(self, questions, category, player_answers=None):
        self.questions = questions
        self.category = category
        self.playerAnswers = player_answers if player_answers is not None else defaultdict(list)

    def count_correct_answers(self, username):
        correct_answers = 0

        for i, question in enumerate(self.questions):
            if username in self.playerAnswers:
                if question.answer == self.playerAnswers[username][i]:
                    correct_answers += 1

        return correct_answers

    def to_dict(self):
        return {
            "questions": [question.to_dict() for question in self.questions],
            "category": self.category.toJSON(),
            "playerAnswers": dict(self.playerAnswers)
        }

    @staticmethod
    def fromJSON(json_str):
        parsed_json = json.loads(json_str)

        questions = [Question.fromJSON(json.dumps(question)) for question in parsed_json["questions"]]
        category = Category.fromJSON(json.dumps(parsed_json["category"]))

        return Turn(questions, category, parsed_json.get("playerAnswers", {}))
