from bibleduel.service.categorie_service import CategorieService
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from bibleduel.service.guard_service import GuardService


def category_routes(app, db):
    category_service = CategorieService(db)

    @app.route('/turn', methods=['GET'])
    @jwt_required()
    def get_new_turn_data_2():
        return category_service.get_new_turn_data()

    @app.route('/api/turn', methods=['GET'])
    @jwt_required()
    def get_new_turn_data():
        return category_service.get_new_turn_data()

    @app.route('/categories', methods=['GET'])
    @jwt_required()
    def get_list_of_categories_2():
        return category_service.get_list_of_categories()

    @app.route('/api/categories', methods=['GET'])
    @jwt_required()
    def get_list_of_categories():
        return category_service.get_list_of_categories()

    @app.route('/api/categories', methods=['POST'])
    @jwt_required()
    def add_category():
        user_id = get_jwt_identity()
        if GuardService.is_admin(user_id, db):
            data = request.json
            return category_service.add_category(user_id, data)

    @app.route('/api/categories/<string:category_id>', methods=['PUT'])
    @jwt_required()
    def edit_category(category_id):
        user_id = get_jwt_identity()
        if GuardService.is_admin(user_id, db):
            category = request.json
            return category_service.edit_category(user_id, category_id, category)

    @app.route('/api/categories/<string:category_id>', methods=['DELETE'])
    @jwt_required()
    def delete_category(category_id):
        user_id = get_jwt_identity()
        if GuardService.is_admin(user_id, db):
            return category_service.delete_category(category_id)
