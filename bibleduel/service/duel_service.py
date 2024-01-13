import re
from flask import jsonify
from bibleduel.models.player import Player


class DuelService:

    def __init__(self, db):
        self.db = db

    def get_duel_list(self, user_id):
        pass

    def create_duel(self, user_id, opponent_id):
        pass

    def update_duel(self, user_id, duel):
        pass

    def delete_duel(self, user_id, duel_id):
        pass
