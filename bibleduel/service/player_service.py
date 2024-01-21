import re
from flask import jsonify
from bibleduel.models.player import Player


class PlayerService:

    def __init__(self, db):
        self.db = db

    def findPlayer(self, player_name):
        if not player_name:
            return jsonify([])

        regex_pattern = re.compile(re.escape(player_name), re.IGNORECASE)
        query = {"username": {"$regex": regex_pattern}}
        users = list(self.db["user"].find(query))

        players = [Player.user_to_player_json(user) for user in users]

        return jsonify({
            "players": players,
            "msg": f"{len(players)} Spieler gefunden",
        }), 200

    def addFriend(self, user_id, player_id):
        print("called")
        player = Player.user_to_player_json(self.db["user"].find_one({"_id": player_id}))

        if not player:
            return jsonify({
                "msg": "Spieler nicht gefunden"
            }), 404

        if player_id == user_id:
            return jsonify({
                "msg": "Du kannst dich nicht selbst hinzufügen"
            }), 400

        self.db["user"].update_one({"_id": user_id}, {"$addToSet": {"friends": player}})

        return jsonify({
            "msg": "Spieler hinzugefügt"
        }), 200

    def removeFriend(self, user_id, player_id):
        player = Player.user_to_player_json(self.db["user"].find_one({"_id": player_id}))

        if not player:
            return jsonify({
                "msg": "Spieler nicht gefunden"
            }), 404

        if player_id == user_id:
            return jsonify({
                "msg": "Du kannst dich nicht selbst entfernen"
            }), 400

        self.db["user"].update_one({"_id": user_id}, {"$pull": {"friends": {"_id": player_id}}})

        return jsonify({
            "msg": "Spieler entfernt"
        }), 200
