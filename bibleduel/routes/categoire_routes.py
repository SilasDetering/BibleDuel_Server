from bibleduel.service.categorie_service import CategorieService
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity


def category_routes(app, db):
    category_service = CategorieService(db)

    @app.route('/turn', methods=['GET'])
    @jwt_required()
    def get_new_turn_data():
        return category_service.get_new_turn_data()

    @app.route('/categories', methods=['GET'])
    @jwt_required()
    def get_list_of_categories():
        return category_service.get_list_of_categories()

    @app.route('/categories', methods=['POST'])
    @jwt_required()
    def add_category():
        user_id = get_jwt_identity()
        data = request.json
        new_category = data.get('category')
        return category_service.add_category(user_id, new_category)

    @app.route('/categories/<string:category>', methods=['DELETE'])
    @jwt_required()
    def delete_category(category):
        user_id = get_jwt_identity()
        return category_service.delete_category(user_id, category)
