from src import app
from src.vital import core
from flask import make_response, request, jsonify
from src.service import user as service

# ===============
# get user profile
# ===============
# TODO wip NO NEED ?
getprofile_schema = {
    'user_name': {
        'type': 'string',
        'required': True,
        'empty': False,
        'maxlength': 200
    },
    'mail_address': {
        'type': 'string',
        'required': True,
        'empty': False,
        'regex': '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9_.+-]+$',
        'maxlength': 200
    },
    'password': {
        'type': 'string',
        'required': True,
        'minlength': 8,
        'maxlength': 200
    }
}


# @core.validation(getprofile_schema)
@app.route('/user/profile', methods=['POST'])
@core.authentication()
def getprofile():
    user_id = request.headers.get('x-auth-header', '')
    res = service.get_user_profile(user_id)
    return jsonify(res), 200
