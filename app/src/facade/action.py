from src import app
from src.vital import core
from flask import make_response, request, jsonify
from src.service import action as service

# ===============
# get user profile
# ===============
book_rental = {
    'book_id': {
        'required': True
    },
    'num': {
        'required': True
    }
}


@core.validation(book_rental)
@app.route('/action/rental', methods=['POST'])
@core.authentication()
def rental():
    user_id = request.headers.get('x-auth-header', '')
    req = request.json
    res = service.rental(user_id, req)
    return jsonify(res), 200


@core.validation(book_rental)
@app.route('/action/return', methods=['POST'])
@core.authentication()
def book_return():
    user_id = request.headers.get('x-auth-header', '')
    req = request.json
    res = service.book_return(user_id, req)
    return jsonify(res), 200
