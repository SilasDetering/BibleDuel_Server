from authentication.auth_service import AuthService
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity



def auth_routes(app, db):
    auth_service = AuthService(db)

    @app.route('/user', methods=['POST'])
    def register():
        username = request.json['username']
        password = request.json['password']

        return auth_service.register(username, password)

    @app.route('/user', methods=['PUT'])
    def login():
        username = request.json['username']
        password = request.json['password']

        return auth_service.login(username, password)

    @app.route('/user', methods=['GET'])
    @jwt_required()
    def refresh():
        user_id = get_jwt_identity()
        return auth_service.refresh(user_id)

    @app.route('/user/username', methods=['PUT'])
    @jwt_required()
    def change_username():
        user_id = get_jwt_identity()
        data = request.json
        new_username = data.get('new_username')
        return auth_service.change_username(new_username, user_id)

    @app.route('/user/password', methods=['PUT'])
    @jwt_required()
    def change_password():
        user_id = get_jwt_identity()
        data = request.json
        old_pw = data.get('old_password')
        new_pw = data.get('new_password')
        return auth_service.change_password(old_pw, new_pw, user_id)
