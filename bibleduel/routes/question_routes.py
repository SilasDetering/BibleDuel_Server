from bibleduel.service.question_service import QuestionService
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity


def question_routes(app, db):
    question_service = QuestionService(db)

    @app.route('/questions', methods=['GET'])
    @jwt_required()
    def get_new_turn_data():
        return question_service.get_new_turn_data()

    @app.route('/categories', methods=['GET'])
    @jwt_required()
    def get_list_of_categories():
        return question_service.get_list_of_categories()

    @app.route('/questions', methods=['POST'])
    @jwt_required()
    def add_question():
        user_id = get_jwt_identity()
        data = request.json
        new_question = data.get('question')
        return question_service.add_question(user_id, new_question)

    @app.route('/categories', methods=['POST'])
    @jwt_required()
    def add_category():
        user_id = get_jwt_identity()
        data = request.json
        new_category = data.get('category')
        return question_service.add_category(user_id, new_category)

    @app.route('/questions/<string:question_id>', methods=['DELETE'])
    @jwt_required()
    def delete_question(question_id):
        user_id = get_jwt_identity()
        return question_service.delete_question(user_id, question_id)

    @app.route('/categories/<string:category>', methods=['DELETE'])
    @jwt_required()
    def delete_category(category):
        user_id = get_jwt_identity()
        return question_service.delete_category(user_id, category)
