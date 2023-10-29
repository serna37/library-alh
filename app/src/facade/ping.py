from src import app
from src.vital import core
from flask import jsonify

@app.route('/ping', methods=['GET'])
@core.authentication()
def ping():
    return jsonify('ok'), 200
