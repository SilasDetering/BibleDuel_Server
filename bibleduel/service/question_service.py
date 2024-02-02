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
        projection = {"_id": 0}
        list_of_categories = list(self.db["categories"].find(projection=projection))
        selected_categories = random.sample(list_of_categories, 3)

        turns = []

        for category in selected_categories:
            questions = list(self.db["questions"].find({"category": category["title"]}))

            print(category["title"])
            print(questions)

            # Ziehe drei zufällige Fragen aus der Liste
            selected_questions = random.sample(questions, 3)

            # Mische die Antworten
            for question in selected_questions:
                random.shuffle(question["options"])

            # Ersetze die Katgegorie-Titel im Question-Objekt durch das Katgegorie-Objekt
            for question in selected_questions:
                question["category"] = category

            turn_json = {
                "questions": [question for question in selected_questions],
                "category": category,
            }

            turns.append(turn_json)
        return jsonify({"turns": turns}), 200

    def get_list_of_categories(self):
        projection = {"_id": 0}
        list_of_categories = list(self.db["categories"].find(projection=projection))
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
        new_question_title = new_question['category']['title']
        new_question['category'] = new_question_title

        self.db["questions"].insert_one(new_question)

        return jsonify({"msg": "Frage hinzugefügt"}), 200

    def add_category(self, user_id, new_category):
        user = self.db["user"].find_one({"_id": user_id})

        if user is None:
            return jsonify({"error": "User not found"}), 404
        if user["role"] != "admin":
            return jsonify({"error": "User is not admin"}), 403

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
