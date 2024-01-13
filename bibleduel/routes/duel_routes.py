from bibleduel.models.duel import Duel
from bibleduel.service.duel_service import DuelService
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity


def duel_routes(app, db):
    duel_service = DuelService(db)

    @app.route('/game/duel_list', methods=['GET'])
    @jwt_required()
    def get_duel_list():
        user_id = get_jwt_identity()
        return duel_service.get_duel_list(user_id)

    @app.route('/game/duel', methods=['POST'])
    @jwt_required()
    def create_duel():
        user_id = get_jwt_identity()
        data = request.json
        opponent_id = data.get('opponent_id')
        return duel_service.create_duel(user_id, opponent_id)

    @app.route('/game/duel', methods=['PUT'])
    @jwt_required()
    def update_duel():
        user_id = get_jwt_identity()
        data = request.json
        duel = data.get('duel')
        return duel_service.update_duel(user_id, duel)

    @app.route('/game/duel', methods=['DELETE'])
    @jwt_required()
    def delete_duel():
        user_id = get_jwt_identity()
        data = request.json
        duel_id = data.get('duel_id')
        return duel_service.delete_duel(user_id, duel_id)
