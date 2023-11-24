from flask import jsonify, request, session
from passlib.hash import pbkdf2_sha256
from app import db
import uuid

class User:

    def signup(self):
        # Create the user object
        user = {
            "_id": uuid.uuid4().hex,
            "username": request.json['username'],
            "password": request.json['password']
        }

        # Encrypt the password
        user['password'] = pbkdf2_sha256.encrypt(user['password'])

        # Check for existing username
        if db.user.find_one({ "username": user['username'] }):
            return jsonify({ "error": "Username already exists" }), 400

        if db.user.insert_one(user):
            return self.create_session(user)

        return jsonify({ "error": "Signup failed" }), 400
    
    def create_session(self, user):
        del user['password']
        session['logged_in'] = True
        session['user'] = user
        return jsonify(user), 200
    
    def signout(self):
        session.clear()
        return jsonify({ "message": "Successfully signed out" }), 200
    
    def login(self):

        user = db.user.find_one({
            "username": request.json['username']
        })

        if user and pbkdf2_sha256.verify(request.json['password'], user['password']):
            return self.start_session(user)
        
        return jsonify({ "error": "Invalid login credentials" }), 401