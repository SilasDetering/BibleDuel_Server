import re
from flask import jsonify
from bibleduel.models.player import Player


class PlayerService:

    def __init__(self, db):
        self.db = db

    def findPlayer(self, player_name, user_id):
        if not player_name:
            return jsonify([]), 200

        user = self.db["user"].find_one({"_id": user_id})

        if user is None:
            return jsonify({"error": "Benutzer nicht gefunden"}), 404

        friend_ids = user.get("friends", {}).keys()

        regex_pattern = re.compile(re.escape(player_name), re.IGNORECASE)
        query = {"username": {"$regex": regex_pattern}}
        users = list(self.db["user"].find(query))

        players = []
        for user in users:
            if user["_id"] not in friend_ids and user["_id"] != user_id:
                player = Player.user_to_player_dict(user)
                players.append(player)

        return jsonify({
            "players": players,
            "msg": f"{len(players)} Spieler gefunden",
        }), 200

    def addFriend(self, user_id, player_id):
        player = self.db["user"].find_one({"_id": player_id})

        if not player:
            return jsonify({
                "msg": "Spieler nicht gefunden"
            }), 404

        if player_id == user_id:
            return jsonify({
                "msg": "Du kannst dich nicht selbst hinzufügen"
            }), 400

        user_friends = self.db["user"].find_one({"_id": user_id})["friends"]
        if user_friends and player_id in user_friends:
            return jsonify({
                "msg": "Der Spieler ist bereits dein Freund"
            }), 400

        self.db["user"].update_one(
            {"_id": user_id},
            {"$set": {f"friends.{player_id}": [0, 0, 0]}}
        )

        return jsonify({
            "msg": "Spieler hinzugefügt"
        }), 200

    def removeFriend(self, user_id, player_id):

        update_query = {
            "$unset": {
                f"friends.{player_id}": 1
            }
        }

        search_query = {"_id": user_id}

        result = self.db["user"].update_one(search_query, update_query)

        if result.modified_count == 1:
            return {
                "msg": "Spieler entfernt"
            }, 200
        else:
            return {
                "msg": "Benutzer oder Spieler nicht gefunden"
            }, 404

    def get_friends(self, user_id):
        user = self.db["user"].find_one({"_id": user_id})

        if not user:
            return jsonify({
                "msg": "Benutzer nicht gefunden"
            }), 404

        friends = []

        for friend_id in user["friends"]:
            friend = self.db["user"].find_one({"_id": friend_id})
            if friend:
                friend_data = Player.user_to_player_dict(friend)
                friend_data["ratio"] = [
                    user["friends"][friend["_id"]][0],
                    user["friends"][friend["_id"]][1],
                    user["friends"][friend["_id"]][2]
                ]
                friends.append(friend_data)
            else:
                self.db["user"].update_one(
                    {"_id": user_id},
                    {"$unset": {f"friends.{friend_id}": 1}}
                )

        return jsonify({
            "friends": friends
        }), 200
