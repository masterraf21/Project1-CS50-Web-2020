from flask import render_template, jsonify
from app import app,db

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": 404})


@app.errorhandler(500)
def internal_server_error(error):
    pass