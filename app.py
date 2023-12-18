from flask import Flask
from flask_jwt_extended import JWTManager
from pymongo import MongoClient
from settings import MONGO_URI

from authentication.auth_routes import register_auth_routes
from bibleduel.routes.player_routes import register_player_routes

# Flask
app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'secret'
app.config['JWT_ALGORITHM'] = 'HS256'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
jwt = JWTManager(app)

# Database
mongoDB = MongoClient(MONGO_URI)["bibleduel"]

# Routes
register_auth_routes(app, mongoDB)
register_player_routes(app, mongoDB)

if __name__ == '__main__':
    app.run(debug=True)
