from bibleduel.service.player_service import PlayerService
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity


def register_player_routes(app, db):
    player_service = PlayerService(db)

    @app.route('/user/find/', methods=['GET'])
    @jwt_required()
    def find_player():
        player_name = request.args.get('player_name')
        return player_service.findPlayer(player_name)

    @app.route('/user/addFriend', methods=['PUT'])
    @jwt_required()
    def add_friend():
        user_id = get_jwt_identity()
        data = request.json
        player_id = data.get('player_id')
        return player_service.addFriend(user_id, player_id)

    @app.route('/user/removeFriend', methods=['PUT'])
    @jwt_required()
    def remove_friend():
        user_id = get_jwt_identity()
        data = request.json
        player_id = data.get('player_id')
        return player_service.removeFriend(user_id, player_id)
