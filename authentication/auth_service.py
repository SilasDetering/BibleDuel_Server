import os
from flask import jsonify
from flask_jwt_extended import create_access_token
from passlib.hash import pbkdf2_sha256
from settings import PEPPER, HASHROUNDS
from bibleduel.models.user import User
import re


class AuthService:

    def __init__(self, db):
        self.db = db

    @staticmethod
    def generate_salt():
        return os.urandom(16).hex()

    def register(self, username, password):
        # Create the user object
        new_user = User(None, username, password, None, None, None, salt=self.generate_salt())

        # Verify the user object
        val = new_user.validate_username()
        val = new_user.validate_password() if val is None else val
        if val is not None:
            return jsonify({"msg": val}), 400

        # Encrypt the password
        new_user.password = (pbkdf2_sha256.using(rounds=HASHROUNDS, salt=new_user.salt.encode('utf-8'))
                             .hash(new_user.password + PEPPER))

        # Check for existing username
        if self.db["user"].find_one({"username": {"$regex": f'^{re.escape(new_user.username)}$', "$options": "i"}}):
            return jsonify({"msg": "Benutzername existiert bereits"}), 400

        if self.db["user"].insert_one(new_user.to_dict()):
            access_token = create_access_token(identity=new_user._id)
            return jsonify({
                "msg": "Benutzer erfolgreich registriert",
                "access_token": access_token,
                "user": new_user.to_transmit_dict()
            }), 201

        return jsonify({"msg": "Registrierung fehlgeschlagen"}), 400

    def login(self, username, password):
        query = {"username": username}
        user = self.db["user"].find_one(query)

        if not user:
            return jsonify({"msg": "Ungültige Anmeldedaten"}), 401

        user = User.fromJSON(user)

        if user and pbkdf2_sha256.verify(password + PEPPER, user.password):
            access_token = create_access_token(identity=user._id)
            return jsonify({
                "msg": "Login erfolgreich",
                "access_token": access_token,
                "user": user.to_transmit_dict()
            }), 200
        else:
            return jsonify({"msg": "Ungültige Anmeldedaten"}), 401

    def delete_user(self, user_id):
        user = self.db["user"].find_one({"_id": user_id})

        if user:
            self.db["user"].delete_one({"_id": user_id})
            return jsonify({"msg": "Benutzer erfolgreich gelöscht"}), 200
        else:
            response = jsonify({"msg": "Benutzer konnte nicht gelöscht werden"})
            response.status_code = 404
            return response

    def refresh(self, user_id):
        user = self.db["user"].find_one({"_id": user_id})

        if not user:
            return jsonify({"msg": "Benutzer nicht gefunden"}), 404

        return jsonify({
            "user": User.fromJSON(user).to_transmit_dict()
        }), 200

    def change_password(self, old_pw, new_pw, user_id):
        user = self.db["user"].find_one({"_id": user_id})

        user = User.fromJSON(user)

        if user and pbkdf2_sha256.verify(old_pw + PEPPER, user.password):
            user.password = new_pw

            val = user.validate_password()
            if val is not None:
                return jsonify({"msg": val}), 400

            user.password = (pbkdf2_sha256.using(rounds=HASHROUNDS, salt=user.salt.encode('utf-8'))
                             .hash(user.password + PEPPER))

            self.db["user"].replace_one({"_id": user_id}, user.to_dict())
            return jsonify({"msg": "Passwort erfolgreich geändert"}), 200

        return jsonify({"msg": "Ungültige Anmeldedaten"}), 401

    def change_username(self, new_username, user_id):
        user = self.db["user"].find_one({"_id": user_id})

        if user:
            user = User.fromJSON(user)
            user.username = new_username

            val = user.validate_username()
            if val is not None:
                return jsonify({"msg": val}), 400

            self.db["user"].replace_one({"_id": user_id}, user.to_dict())
            return jsonify({"msg": "Benutzername erfolgreich geändert"}), 200

        return jsonify({"msg": "Benutzername konnte nicht geändert werden"}), 400
