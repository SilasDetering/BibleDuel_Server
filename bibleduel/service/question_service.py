import uuid
from flask import jsonify


class QuestionService:

    def __init__(self, db):
        self.db = db

    def get_question_list(self):
        questions = list(self.db["questions"].find())
        return jsonify(questions), 200

    def get_question(self, question_id):
        question = self.db["questions"].find_one({"_id": question_id})
        return jsonify(question), 200

    def add_question(self, user_id, new_question):
        user = self.db["user"].find_one({"_id": user_id})

        new_question['_id'] = uuid.uuid4().hex
        new_question['category'] = new_question['category']['_id']
        new_question["author"] = user["_id"]

        self.db["questions"].insert_one(new_question)

        return jsonify({"msg": "Frage hinzugefügt"}), 200

    def edit_question(self, question_id, new_question, user_id):

        print(new_question)

        new_question['category'] = new_question['category']['_id']
        new_question["author"] = user_id

        self.db["questions"].replace_one({"_id": question_id}, new_question)
        return jsonify({"msg": "Frage geändert"}), 200

    def delete_question(self, question_id):
        self.db["questions"].delete_one({"_id": question_id})
        return jsonify({"msg": "Frage gelöscht"}), 200

    def report_question(self, user_id, report):
        user = self.db["user"].find_one({"_id": user_id})

        report["_id"] = uuid.uuid4().hex

        if user is None:
            return jsonify({"error": "User not found"}), 404

        question = self.db["questions"].find_one({"_id": report["question_id"]})

        if "reports" not in question:
            self.db["questions"].update_one({"_id": report["question_id"]}, {"$set": {"reports": [report]}})
        else:
            self.db["questions"].update_one({"_id": report["question_id"]}, {"$push": {"reports": report}})

        return jsonify({"msg": "Frage gemeldet"}), 200

    def get_reports(self):
        questions = list(self.db["questions"].find({"reports": {"$exists": True, "$not": {"$size": 0}}}))
        return jsonify(questions), 200

    def delete_report(self, report_id):
        self.db["questions"].update_one({"reports._id": report_id}, {"$pull": {"reports": {"_id": report_id}}})
        return jsonify({"msg": "Report gelöscht"}), 200