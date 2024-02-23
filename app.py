from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager
from pymongo import MongoClient
from settings import MONGO_URI, JWT_SECRET, LATEST_APP_VERSION

from authentication.auth_routes import auth_routes
from bibleduel.routes.player_routes import player_routes
from bibleduel.routes.duel_routes import duel_routes
from bibleduel.routes.question_routes import question_routes

# Flask
app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = JWT_SECRET
app.config['JWT_ALGORITHM'] = 'HS256'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
jwt = JWTManager(app)

# Database
mongoDB = MongoClient(MONGO_URI)["bibleduel"]


# Routes
@app.before_request
def check_app_version():
    app_version = request.headers.get('App-Version')

    if app_version is None or app_version == 'undefined':
        return jsonify({"msg": "App-Version header is missing"}), 400

    app_major, app_minor, app_patch = map(int, app_version.split('.'))
    latest_major, latest_minor, latest_patch = map(int, LATEST_APP_VERSION.split('.'))

    if app_major != latest_major:
        return jsonify({"msg": "Please update the app to the latest version"}), 409


auth_routes(app, mongoDB)
player_routes(app, mongoDB)
duel_routes(app, mongoDB)
question_routes(app, mongoDB)

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=5000)
