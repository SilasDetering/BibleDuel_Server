import json
from datetime import datetime

from bibleduel.models.player import Player
from bibleduel.models.turn import Turn


class Duel:
    def __init__(self, _id, players, current_player, game_state, turns, current_turn, last_edit=None, created_at=None):
        self._id = _id
        self.players = players
        self.current_player = current_player
        self.game_state = game_state
        self.turns = turns
        self.current_turn = current_turn
        self.last_edit = last_edit if last_edit is not None else datetime.now()
        self.created_at = created_at if created_at is not None else datetime.now()

    def toJSON(self):
        return {
            "id": self._id,
            "players": [player.toJSON() for player in self.players],
            "currentPlayer": self.current_player,
            "turns": [turn.toJSON() for turn in self.turns],
            "current_turn": self.current_turn,
        }

    @staticmethod
    def fromJSON(json_str):
        parsed_json = json.loads(json_str)

        players = [Player.fromJSON(json.dumps(player)) for player in parsed_json["players"]]
        turns = [Turn.fromJSON(json.dumps(turn)) for turn in parsed_json["turns"]]

        return Duel(parsed_json["id"], players, parsed_json["currentPlayer"], parsed_json["game_state"], turns,
                    parsed_json["current_turn"])
