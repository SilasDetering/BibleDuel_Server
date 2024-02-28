from flask import jsonify


class GuardService:
    @staticmethod
    def is_admin(user_id, db):
        user = db["user"].find_one({"_id": user_id})

        if user is None:
            return jsonify({"error": "User not found"}), 404
        if user["role"] != "admin":
            return jsonify({"error": "User is not admin"}), 403
        return True
