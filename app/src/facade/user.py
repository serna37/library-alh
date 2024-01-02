from src import app
from src.vital import core
from flask import make_response, request, jsonify
from src.service import user as service

# ===============
# get user profile
# ===============
@app.route('/user/profile', methods=['POST'])
@core.authentication()
def getprofile():
    user_id = request.headers.get('x-auth-header', '')
    res = service.get_user_profile(user_id)
    return jsonify(res), 200


@app.route('/user/rentalstate', methods=['POST'])
@core.authentication()
def getrentalstate():
    user_id = request.headers.get('x-auth-header', '')
    res = service.get_rental_state(user_id)
    return jsonify(res), 200
