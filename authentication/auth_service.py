import os
from flask import jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from passlib.hash import pbkdf2_sha256
from settings import PEPPER, HASHROUNDS
from bibleduel.models.user import User


class AuthService:

    def __init__(self, db):
        self.db = db

    @staticmethod
    def generate_salt():
        return os.urandom(16).hex()

    def register(self):
        # Create the user object
        new_user = User(request.json['username'], request.json['password'], self.generate_salt())

        # Verify the user object
        val = new_user.validate()
        if not val[0]:
            return jsonify({"error": "" + val[1]}), 400

        # Encrypt the password
        new_user.password = (pbkdf2_sha256.using(rounds=HASHROUNDS, salt=new_user.salt.encode('utf-8'))
                             .hash(new_user.password + PEPPER))

        # Check for existing username
        if self.db["user"].find_one({"username": new_user.username}):
            return jsonify({"error": "Benutzername existiert bereits"}), 400

        if self.db["user"].insert_one(new_user.to_json()):
            access_token = create_access_token(identity=new_user.id)
            return jsonify({
                "msg": "Benutzer erfolgreich registriert",
                "access_token": access_token,
                "user": new_user.to_transmit_json()
            }), 201

        return jsonify({"error": "Registrierung fehlgeschlagen"}), 400

    def login(self):

        username = request.json['username']
        password = request.json['password']

        user = self.db["user"].find_one({"username": username})

        user = User.from_json(user)

        if user and pbkdf2_sha256.verify(password + PEPPER, user.password):
            access_token = create_access_token(identity=user.id)
            return jsonify({
                "msg": "Login erfolgreich",
                "access_token": access_token,
                "user": user.to_transmit_json()
            }), 200
        else:
            return jsonify({"error": "Ungültige Anmeldedaten"}), 401

    @jwt_required
    def delete_user(self):
        current_user_id = get_jwt_identity()

        user = self.db["user"].find_one({"_id": current_user_id})

        if user:
            self.db["user"].delete_one({"_id": current_user_id})
            return jsonify({"msg": "Benutzer erfolgreich gelöscht"}), 200
        else:
            return jsonify({"error": "Benutzer konnte nicht gelöscht werden"}), 404
