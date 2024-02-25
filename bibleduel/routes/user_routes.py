from bibleduel.service.user_service import UserService
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity


def user_routes(app, db):
    user_service = UserService(db)

    @app.route('/api/user', methods=['GET'])
    @jwt_required()
    def get_user():
        user_id = get_jwt_identity()
        return user_service.get_user(user_id)

    @app.route('/api/user/contributors', methods=['GET'])
    @jwt_required()
    def get_contributors():
        return user_service.get_contributors()
