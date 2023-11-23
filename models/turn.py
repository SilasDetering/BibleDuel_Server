import json
from typing import List, Dict


class Turn:
    def __init__(self, questions: List[Dict], category: str):
        self.questions = questions
        self.category = category
        self.player_answers = {}

    def get_player_score(self):
        player_score = {}

        for player, answers in self.player_answers.items():
            score = sum(1 for answer in answers if answer)
            player_score[player] = score

        return player_score

    def to_json(self):
        return {
            "questions": self.questions,
            "category": self.category,
            "player_answers": self.player_answers,
        }

    def to_json_string(self):
        return json.dumps(self.to_json())

    @staticmethod
    def from_json(json_string):
        parsed_json = json.loads(json_string)

        questions = parsed_json["questions"]
        category = parsed_json["category"]

        turn = Turn(questions, category)

        if "player_answers" in parsed_json and isinstance(parsed_json["player_answers"], dict):
            turn.player_answers = parsed_json["player_answers"]

        return turn
