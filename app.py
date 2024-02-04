from flask import Flask
from flask_jwt_extended import JWTManager
from pymongo import MongoClient
from settings import MONGO_URI, JWT_SECRET

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
auth_routes(app, mongoDB)
player_routes(app, mongoDB)
duel_routes(app, mongoDB)
question_routes(app, mongoDB)

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=5000)

