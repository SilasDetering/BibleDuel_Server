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
            if contributor and contributor["_id"] != "0af22af81bc247a99b289cadc59d60bf":
                contributors.append(Player.user_to_player_dict(contributor))
        return jsonify({
            "contributors": contributors
        }), 200

    def get_user_list(self):
        projection = {"_id": 1, "username": 1, "friends": 1, "score": 1, "role": 1}
        user_list = self.db["user"].find({}, projection)
        user_list = [user for user in user_list]

        return jsonify({
            "user_list": user_list
        }), 200

    def edit_user(self, user_id, new_user):
        user = self.db["user"].find_one({"_id": user_id})

        if user:
            updated_values = {
                "$set": {
                    "score": new_user.get("score", user["score"]),
                    "username": new_user.get("username", user["username"]),
                    "role": new_user.get("role", user["role"])
                }
            }

            self.db["user"].update_one({"_id": user_id}, updated_values)
            return jsonify({"msg": "Benutzer erfolgreich gespeichert"}), 200
        else:
            response = jsonify({"msg": "Benutzer konnte nicht geändert werden"})
            response.status_code = 404
            return response

    def delete_user(self, user_id):
        user = self.db["user"].find_one({"_id": user_id})

        if user:
            self.db["user"].delete_one({"_id": user_id})
            return jsonify({"msg": "Benutzer erfolgreich gelöscht"}), 200
        else:
            response = jsonify({"msg": "Benutzer konnte nicht gelöscht werden"})
            response.status_code = 404
            return response
