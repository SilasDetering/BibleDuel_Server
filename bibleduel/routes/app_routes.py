from flask import Flask, send_file, jsonify


def app_routes(app):
    @app.route('/download/android')
    def download_file():
        return jsonify({"msg": "Download aktuell nicht verfügbar"}), 200