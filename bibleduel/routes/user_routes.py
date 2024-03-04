from flask import request
from bibleduel.service.user_service import UserService
from flask_jwt_extended import jwt_required, get_jwt_identity
from bibleduel.service.guard_service import GuardService


def user_routes(app, db):
    user_service = UserService(db)

    @app.route('/api/user', methods=['GET'])
    @jwt_required()
    def get_user_list():
        user_id = get_jwt_identity()
        if GuardService.is_admin(user_id, db):
            return user_service.get_user_list()

    @app.route('/api/user/<string:user_id>', methods=['PUT'])
    @jwt_required()
    def edit_user(user_id):
        admin_id = get_jwt_identity()
        if GuardService.is_admin(admin_id, db):
            new_user_obj = request.json["new_user_obj"]
            return user_service.edit_user(user_id, new_user_obj)

    @app.route('/user', methods=['DELETE'])
    @jwt_required()
    def delete_2():
        user_id = get_jwt_identity()
        return user_service.delete_user(user_id)

    @app.route('/api/user', methods=['DELETE'])
    @jwt_required()
    def delete():
        user_id = get_jwt_identity()
        return user_service.delete_user(user_id)

    @app.route('/api/user/<string:user_id>', methods=['DELETE'])
    @jwt_required()
    def delete_user(user_id):
        admin_id = get_jwt_identity()
        if GuardService.is_admin(admin_id, db):
            return user_service.delete_user(user_id)

    @app.route('/user/contributors', methods=['GET'])
    @jwt_required()
    def get_contributors_2():
        return user_service.get_contributors()

    @app.route('/api/user/contributors', methods=['GET'])
    @jwt_required()
    def get_contributors():
        return user_service.get_contributors()
