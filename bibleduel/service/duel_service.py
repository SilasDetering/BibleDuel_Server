import json
import random
from flask import jsonify
from bibleduel.models.player import Player
from bibleduel.models.duel import Duel
from bibleduel.models.user import User
from datetime import date, datetime, timedelta


class DuelService:

    def __init__(self, db):
        self.db = db

    def get_duel_list(self, user_id):
        query = {"players._id": user_id}
        duel_list = list(self.db["duels"].find(query))
        reload_list = False

        for duel in duel_list:
            diff = datetime.now() - duel["last_edit"]

            # Laufende Duelle nach 7 Tagen inaktivität löschen
            if diff > timedelta(days=7):
                query = {"_id": duel["_id"]}
                self.db["duels"].delete_one(query)
                reload_list = True

            # Beendete Duelle nach 3 Tagen löschen
            if duel["game_state"] == 0 or duel["game_state"] == 2:
                if diff > timedelta(days=3):
                    query = {"_id": duel["_id"]}
                    self.db["duels"].delete_one(query)
                    reload_list = True

        if reload_list:
            duel_list = list(self.db["duels"].find(query))

        return jsonify(duel_list), 200

    def get_duel(self, duel_id, user_id):
        query = {"_id": duel_id, "players._id": user_id}
        duel = self.db["duels"].find_one(query)

        if duel is None:
            return jsonify({"error": "Duel not found"}), 404

        return jsonify(duel), 200

    def create_duel(self, user_id, opponent_id):
        if user_id == opponent_id:
            return jsonify({"error": "You can't duel yourself"}), 400

        user = self.db["user"].find_one({"_id": user_id})
        opponent = self.db["user"].find_one({"_id": opponent_id})

        if user is None or opponent is None:
            return jsonify({"error": "User not found"}), 404

        user_player = Player.user_to_player(user)
        opponent_player = Player.user_to_player(opponent)

        duel = Duel.create_new_duel(user_player, opponent_player)
        self.db["duels"].insert_one(duel.to_dict())

        return jsonify(duel.to_dict()), 200

    def challenge_random_player(self, user_id):
        users = list(self.db["user"].find({"_id": {"$ne": user_id}}))

        if not users:
            return jsonify({"error": "No other users found"}), 404

        opponent = random.choice(users)

        return self.create_duel(user_id, opponent["_id"])

    def update_duel(self, user_id, duel):
        if isinstance(duel, str):
            duel_dict = json.loads(duel)
        else:
            duel_dict = duel

        duel_id = duel_dict["_id"]
        query = {"_id": duel_id}
        old_duel_dict = self.db["duels"].find_one(query)

        if old_duel_dict is None:
            return jsonify({"error": "Duel not found"}), 404

        old_duel = Duel.fromJSON(old_duel_dict)
        new_duel = Duel.fromJSON(duel_dict)

        if old_duel.players[old_duel.current_player]._id != user_id:
            return jsonify({"error": "Not your turn"}), 403

        if old_duel.game_state > 1:
            return jsonify({"error": "Game is over"}), 403

        new_duel.last_edit = datetime.now()
        new_duel.created_at = old_duel_dict["created_at"]

        self.db["duels"].replace_one(query, new_duel.to_dict())

        if new_duel.game_state > 1:
            self.update_stats(new_duel)

        return jsonify({"msg": "Duell aktualisiert"}), 200

    def delete_duel(self, user_id, duel_id):
        query = {"_id": duel_id}
        projection = {"created_at": 0, "last_edit": 0}
        old_duel_dict = self.db["duels"].find_one(query, projection)

        if old_duel_dict is None:
            return jsonify({"msg": "Duell nicht mehr vorhanden"}), 200

        old_duel = Duel.fromJSON(json.dumps(old_duel_dict))

        if old_duel.players[0]._id != user_id and old_duel.players[1]._id != user_id:
            return jsonify({"error": "Not your duel"}), 403

        self.db["duels"].delete_one(query)
        return jsonify({"msg": "Duell gelöscht"}), 200

    def update_stats(self, duel: Duel):
        player_score = duel.get_score()

        user_winner = None
        user_loser = None

        if player_score[duel.players[0]._id] > player_score[duel.players[1]._id]:
            user_winner = User.fromJSON(self.db["user"].find_one({"_id": duel.players[0]._id}))
            user_loser = User.fromJSON(self.db["user"].find_one({"_id": duel.players[1]._id}))

        elif player_score[duel.players[0]._id] < player_score[duel.players[1]._id]:
            user_winner = User.fromJSON(self.db["user"].find_one({"_id": duel.players[1]._id}))
            user_loser = User.fromJSON(self.db["user"].find_one({"_id": duel.players[0]._id}))

        if user_loser is not None and user_winner is not None:

            if user_winner.friends.get(user_loser._id):
                user_winner.friends[user_loser._id][0] += 1

            if user_loser.friends.get(user_winner._id):
                user_loser.friends[user_winner._id][1] += 1

            user_winner.score += 20

            if (user_loser.score - 10 < 0):
                user_loser.score = 0
            else:
                user_loser.score -= 10

            self.db["user"].replace_one({"_id": user_winner._id}, user_winner.to_dict())
            self.db["user"].replace_one({"_id": user_loser._id}, user_loser.to_dict())

        else:
            user_one = User.fromJSON(self.db["user"].find_one({"_id": duel.players[1]._id}))
            user_two = User.fromJSON(self.db["user"].find_one({"_id": duel.players[0]._id}))

            if user_one.friends.get(user_two._id):
                user_one.friends[user_two._id][2] += 1
            if user_two.friends.get(user_one._id):
                user_two.friends[user_one._id][2] += 1

            user_one.score += 10
            user_two.score += 10

            self.db["user"].replace_one({"_id": user_one._id}, user_one.to_dict())
            self.db["user"].replace_one({"_id": user_two._id}, user_two.to_dict())

    def get_duel_count(self):
        number_of_duels = self.db["duels"].count_documents({})
        return jsonify({"duel_count": number_of_duels}), 200
