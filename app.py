from flask import Flask
from flask_jwt_extended import JWTManager
from pymongo import MongoClient
from settings import MONGO_URI

app = Flask(__name__)
app.secret_key = 'secret'

# Database
mongoDB = MongoClient(MONGO_URI)["user"]
jwt = JWTManager(app)

# Routes
from authentication.auth_routes import register_routes

register_routes(app, mongoDB)

if __name__ == '__main__':
    app.run(debug=True)
