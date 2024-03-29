import os

from flask import Flask, request, jsonify, send_from_directory
from flask_jwt_extended import JWTManager
# from flask_cors import CORS
from pymongo import MongoClient
from settings import MONGO_URI, JWT_SECRET, LATEST_APP_VERSION

from authentication.auth_routes import auth_routes
from bibleduel.routes.player_routes import player_routes
from bibleduel.routes.duel_routes import duel_routes
from bibleduel.routes.question_routes import question_routes
from bibleduel.routes.user_routes import user_routes
from bibleduel.routes.categoire_routes import category_routes

# Flask
app = Flask(__name__, static_folder='./bibleduel-webapp/dist/bibleduel-webapp')
app.config['JWT_SECRET_KEY'] = JWT_SECRET
app.config['JWT_ALGORITHM'] = 'HS256'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
jwt = JWTManager(app)

# Database
mongoDB = MongoClient(MONGO_URI)["bibleduel"]

# Angular Frontend Path
angular_dist_path = "./bibleduel-webapp/dist/bibleduel-webapp"


# CORS(app)

# Check App-Version
@app.before_request
def check_app_version():
    app_version = request.headers.get('App-Version')
    device = request.headers.get('device')

    if device == 'ios' or device == 'android':
        if app_version is None or app_version == 'undefined':
           return jsonify({"msg": "App-Version header is missing"}), 400

        app_major, app_minor, app_patch = map(int, app_version.split('.'))
        latest_major, latest_minor, latest_patch = map(int, LATEST_APP_VERSION.split('.'))

        if app_major != latest_major:
            return jsonify({"msg": "Please update the app to the latest version"}), 409


# Angular Webapp
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(os.path.join(angular_dist_path, path)):
        return send_from_directory(angular_dist_path, path)
    else:
        return send_from_directory(angular_dist_path, 'index.html')


# Routes
auth_routes(app, mongoDB)
player_routes(app, mongoDB)
duel_routes(app, mongoDB)
question_routes(app, mongoDB)
user_routes(app, mongoDB)
category_routes(app, mongoDB)

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=5000)
