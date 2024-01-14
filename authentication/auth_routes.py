from authentication.auth_service import AuthService
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity


def auth_routes(app, db):
    auth_service = AuthService(db)

    @app.route('/user/register', methods=['POST'])
    def register():
        username = request.json['username']
        password = request.json['password']

        return auth_service.register(username, password)

    @app.route('/user/login', methods=['POST'])
    def login():
        username = request.json['username']
        password = request.json['password']

        return auth_service.login(username, password)

    @app.route('/user/delete', methods=['DELETE'])
    @jwt_required()
    def delete():
        user_id = get_jwt_identity()
        print(user_id)
        return auth_service.delete_user(user_id)

    @app.route('/user/refresh', methods=['GET'])
    @jwt_required()
    def refresh():
        user_id = get_jwt_identity()
        return auth_service.refresh(user_id)
