from flask import render_template
from app import app,db

@app.errorhandler(404)
def not_found_error(error):
    pass


@app.errorhandler(500)
def internal_server_error(error):
    pass