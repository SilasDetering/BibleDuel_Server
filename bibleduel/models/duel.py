import json
import uuid
from datetime import datetime

from bibleduel.models.player import Player
from bibleduel.models.turn import Turn


class Duel:
    score: dict = {}

    def __init__(self, _id: str, players, current_player: int, game_state: int,
                 turns, current_turn: int, last_edit=None, created_at=None):
        self._id = _id
        self.players = players
        self.current_player = current_player
        self.game_state = game_state
        self.turns = turns
        self.current_turn = current_turn
        self.last_edit = last_edit if last_edit is not None else datetime.now()
        self.created_at = created_at if created_at is not None else datetime.now()

    @staticmethod
    def create_new_duel(user: Player, opponent: Player):
        return Duel(uuid.uuid4().hex, [user, opponent], 1, 0, [], 0)

    def get_score(self):
        for player in self.players:
            self.score[player._id] = 0

            for turn in self.turns:
                player_score = turn.count_correct_answers(player.username)
                self.score[player._id] += player_score
        return self.score

    @staticmethod
    def fromJSON(data):
        if isinstance(data, str):
            parsed_json = json.loads(data)
        else:
            parsed_json = data

        players = [Player.fromJSON(json.dumps(player)) for player in parsed_json["players"]]
        turns = [Turn.fromJSON(json.dumps(turn)) for turn in parsed_json["turns"]]

        return Duel(parsed_json["_id"], players, parsed_json["current_player"], parsed_json["game_state"], turns,
                    parsed_json["current_turn"])

    def to_dict(self):
        return {
            "_id": self._id,
            "players": [player.to_dict() for player in self.players],
            "current_player": self.current_player,
            "game_state": self.game_state,
            "turns": [turn.to_dict() for turn in self.turns],
            "current_turn": self.current_turn,
            "last_edit": self.last_edit,
            "created_at": self.created_at
        }
