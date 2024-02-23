import json
import random
import uuid
from collections import defaultdict
from flask import jsonify
from bibleduel.models.question import Question


class QuestionService:

    def __init__(self, db):
        self.db = db

    def get_new_turn_data(self):
        success = False
        errno = 0
        turns = []

        while not success and errno < 10:
            success = True
            turns = []

            list_of_categories = list(self.db["categories"].find())
            selected_categories = random.sample(list_of_categories, 3)

            for category in selected_categories:
                questions = list(self.db["questions"].find({"category": category["_id"]}))

                if len(questions) < 3:
                    print("error aufgetreten")
                    errno += 1
                    success = False
                    continue

                # Ziehe drei zufällige Fragen aus der Liste
                selected_questions = random.sample(questions, 3)

                # Mische die Antworten
                for question in selected_questions:
                    random.shuffle(question["options"])

                # Ersetze die Katgegorie-ID im Question-Objekt durch das Katgegorie-Objekt
                for question in selected_questions:
                    question["category"] = category

                turn_json = {
                    "questions": [question for question in selected_questions],
                    "category": category,
                }

                turns.append(turn_json)

        if errno >= 10:
            return jsonify({"error": "Es konnten keine Duelle erzeugt werden"}), 404

        return jsonify({"turns": turns}), 200

    def get_list_of_categories(self):
        list_of_categories = list(self.db["categories"].find())
        return jsonify({"categories": list_of_categories}), 200

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

    def add_category(self, user_id, new_category):
        user = self.db["user"].find_one({"_id": user_id})

        if user is None:
            return jsonify({"error": "User not found"}), 404
        if user["role"] != "admin":
            return jsonify({"error": "User is not admin"}), 403

        new_category['_id'] = uuid.uuid4().hex
        new_category["author"] = user["_id"]

        self.db["categories"].insert_one(new_category)
        return jsonify({"msg": "Kategorie hinzugefügt"}), 200

    def delete_question(self, user_id, question_id):
        user = self.db["user"].find_one({"_id": user_id})

        if user is None:
            return jsonify({"error": "User not found"}), 404
        if user["role"] != "admin":
            return jsonify({"error": "User is not admin"}), 403

        self.db["questions"].delete_one({"_id": question_id})
        return jsonify({"msg": "Frage gelöscht"}), 200

    def delete_category(self, user_id, category):
        user = self.db["user"].find_one({"_id": user_id})

        if user is None:
            return jsonify({"error": "User not found"}), 404
        if user["role"] != "admin":
            return jsonify({"error": "User is not admin"}), 403

        self.db["categories"].delete_one({"title": category})
        return jsonify({"msg": "Kategorie gelöscht"}), 200

    def get_questions(self, question_id):
        question = self.db["questions"].find_one({"_id": question_id})
        return jsonify(question), 200

    def report_question(self, user_id, report):
        user = self.db["user"].find_one({"_id": user_id})

        if user is None:
            return jsonify({"error": "User not found"}), 404

        question = self.db["questions"].find_one({"_id": report["question_id"]})
        question["reports"].append(report)
        self.db["questions"].update_one({"_id": report["question_id"]}, {"$set": question})
        return jsonify({"msg": "Frage gemeldet"}), 200
