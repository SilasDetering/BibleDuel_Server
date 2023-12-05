import json

from bibleduel.models.player import Player
from bibleduel.models.turn import Turn


class Duel:
    def __init__(self, _id: str, players: list, current_player: int, turns: list, current_turn: int, score: list):
        self.id = _id
        self.players = players
        self.current_player = current_player
        self.turns = turns
        self.current_turn = current_turn
        self.score = score

    def to_json(self):
        return {
            "id": self.id,
            "players": [player.to_json() for player in self.players],
            "currentPlayer": self.current_player,
            "turns": [turn.to_json() for turn in self.turns],
            "currentTurn": self.current_turn,
            "score": self.score
        }

    def to_json_string(self):
        return json.dumps(self.to_json())

    @staticmethod
    def from_json(json_string: str):
        parsed_json = json.loads(json_string)

        players = [Player.from_json(json.dumps(player)) for player in parsed_json["players"]]
        turns = [Turn.from_json(json.dumps(turn)) for turn in parsed_json["turns"]]

        return Duel(
            parsed_json["id"],
            players,
            parsed_json["currentPlayer"],
            turns,
            parsed_json["currentTurn"],
            parsed_json["score"]
        )
