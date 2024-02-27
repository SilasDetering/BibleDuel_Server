import uuid
from flask import jsonify


class QuestionService:

    def __init__(self, db):
        self.db = db

    def get_questions(self, user_id):
        user = self.db["user"].find_one({"_id": user_id})

        if user is None:
            print("error: User not found")
            return jsonify({"error": "User not found"}), 404
        if user["role"] != "admin":
            print("error: User is not admin")
            return jsonify({"error": "User is not admin"}), 403

        questions = list(self.db["questions"].find())
        return jsonify(questions), 200

    def get_question(self, question_id):
        question = self.db["questions"].find_one({"_id": question_id})
        return jsonify(question), 200

    def add_question(self, user_id, new_question):
        user = self.db["user"].find_one({"_id": user_id})

        if user is None:
            print("error: User not found")
            return jsonify({"error": "User not found"}), 404
        if user["role"] != "admin":
            print("error: User is not admin")
            return jsonify({"error": "User is not admin"}), 403

        new_question['_id'] = uuid.uuid4().hex
        new_question['category'] = new_question['category']['_id']
        new_question["author"] = user["_id"]

        self.db["questions"].insert_one(new_question)

        return jsonify({"msg": "Frage hinzugefügt"}), 200

    def delete_question(self, user_id, question_id):
        user = self.db["user"].find_one({"_id": user_id})

        if user is None:
            return jsonify({"error": "User not found"}), 404
        if user["role"] != "admin":
            return jsonify({"error": "User is not admin"}), 403

        self.db["questions"].delete_one({"_id": question_id})
        return jsonify({"msg": "Frage gelöscht"}), 200

    def report_question(self, user_id, report):
        user = self.db["user"].find_one({"_id": user_id})

        if user is None:
            return jsonify({"error": "User not found"}), 404

        question = self.db["questions"].find_one({"_id": report["question_id"]})

        if "reports" not in question:
            self.db["questions"].update_one({"_id": report["question_id"]}, {"$set": {"reports": [report]}})
        else:
            self.db["questions"].update_one({"_id": report["question_id"]}, {"$push": {"reports": report}})

        return jsonify({"msg": "Frage gemeldet"}), 200


