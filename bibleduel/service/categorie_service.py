import uuid
import random
from flask import jsonify


class CategorieService:

    def __init__(self, db):
        self.db = db

    def get_new_turn_data(self):
        success = False
        errno = 0
        turns = []

        while not success and errno < 20:
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

        for category in list_of_categories:
            count = self.db["questions"].count_documents({"category": category["_id"]})
            category["question_count"] = count

        return jsonify({"categories": list_of_categories}), 200

    def add_category(self, user_id, new_category):
        new_category["_id"] = uuid.uuid4().hex
        new_category["author"] = user_id

        self.db["categories"].insert_one(new_category)
        return jsonify({"msg": "Kategorie hinzugefügt"}), 200

    def edit_category(self, user_id, category_id, new_category):
        new_category["author"] = user_id
        self.db["categories"].replace_one({"_id": category_id}, new_category)
        return jsonify({"msg": "Kategorie bearbeitet"}), 200

    def delete_category(self, category_id):
        self.db["categories"].delete_one({"_id": category_id})
        return jsonify({"msg": "Kategorie gelöscht"}), 200
