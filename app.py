from flask import Flask, jsonify
from pymongo import MongoClient


app = Flask(__name__)
app.secret_key = 'secret'

# Database
client = MongoClient('localhost', 27017)
db = client.user

# Routes
from authentication import routes

@app.route('/', methods=['GET'])
def get_data():
    return "Home"

if __name__ == '__main__':
    app.run(debug=True)