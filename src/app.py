from flask import Flask, jsonify
from pymongo import MongoClient

app = Flask(__name__)

client = client = MongoClient("mongodb://localhost:27017/")
db = client['BibleDuel']

@app.route('/api/data', methods=['GET'])
def get_data():
    collection = db['IhreSammlungsName']  # Ersetzen Sie "IhreSammlungsName" durch den tatsächlichen Namen Ihrer Sammlung
    data = list(collection.find())
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)