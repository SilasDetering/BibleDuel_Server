from flask import jsonify
from bibleduel.models.player import Player


class UserService:

    def __init__(self, db):
        self.db = db

    def get_contributors(self):
        contributor_ids = self.db["questions"].distinct("author")
        contributors = []
        for contributor_id in contributor_ids:
            contributor = self.db["user"].find_one({"_id": contributor_id})
            if contributor:
                contributors.append(Player.user_to_player_dict(contributor))
        return jsonify({
            "contributors": contributors
        }), 200

    def get_user(self, user_id):
        user = self.db["user"].find_one({"_id": user_id})

        if not user:
            return jsonify({"msg": "Benutzer nicht gefunden"}), 404

        if user["role"] != "admin":
            return jsonify({"error": "User is not admin"}), 403

        user_list = self.db["user"].find()
        user_list = [user for user in user_list]

        return jsonify({
            "user_list": user_list
        }), 200
