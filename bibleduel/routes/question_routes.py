from bibleduel.service.question_service import QuestionService
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from bibleduel.service.guard_service import GuardService


def question_routes(app, db):
    question_service = QuestionService(db)

    @app.route('/api/questions', methods=['GET'])
    @jwt_required()
    def get_questions():
        user_id = get_jwt_identity()
        if GuardService.is_admin(user_id, db):
            return question_service.get_question_list()

    @app.route('/questions/<string:question_id>', methods=['GET'])
    @jwt_required()
    def get_question(question_id):
        return question_service.get_question(question_id)

    @app.route('/questions', methods=['POST'])
    @jwt_required()
    def add_question():
        user_id = get_jwt_identity()
        if GuardService.is_admin(user_id, db):
            data = request.json
            new_question = data.get('question')
            return question_service.add_question(user_id, new_question)

    @app.route('/api/questions/<string:question_id>', methods=['PUT'])
    @jwt_required()
    def edit_question(question_id):
        user_id = get_jwt_identity()
        if GuardService.is_admin(user_id, db):
            data = request.json
            new_question = data.get('question')
            return question_service.edit_question(question_id, new_question, user_id)

    @app.route('/api/questions/<string:question_id>', methods=['DELETE'])
    @jwt_required()
    def delete_question(question_id):
        user_id = get_jwt_identity()
        if GuardService.is_admin(user_id, db):
            return question_service.delete_question(question_id)

    @app.route('/report', methods=['PUT'])
    @jwt_required()
    def report_question():
        user_id = get_jwt_identity()
        data = request.json
        report = data.get('report')
        return question_service.report_question(user_id, report)

    @app.route('/api/questions/report', methods=['GET'])
    @jwt_required()
    def get_reports():
        user_id = get_jwt_identity()
        if GuardService.is_admin(user_id, db):
            return question_service.get_reports()

    @app.route('/api/questions/report/<string:report_id>', methods=['DELETE'])
    @jwt_required()
    def delete_report(report_id):
        user_id = get_jwt_identity()
        if GuardService.is_admin(user_id, db):
            return question_service.delete_report(report_id)
