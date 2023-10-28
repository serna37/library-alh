from src import app
from src.vital import core
from flask import make_response, request, jsonify
from src.service import sign as service

# ===============
# sign up
# ===============
signup_schema = {
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

@app.route('/sign/up', methods=['POST'])
@core.validation(signup_schema)
def signup():

    ss, mail, token = service.singup(request.json)
    res = make_response(jsonify(ss))

    # header
    res.headers['x-auth-header'] = mail
    # cookie
    res.set_cookie('token', token)
    return res, 200

# ===============
# sign in
# ===============
signin_schema = {
    'mail_address': {
        'type': 'string',
        'required': True
    },
    'password': {
        'type': 'string',
        'required': True
    }
}

@app.route('/sign/in', methods=['POST'])
@core.validation(signin_schema)
def signin():

    ss, mail, token = service.signin(request.json)
    res = make_response(jsonify(ss))

    # header
    res.headers['x-auth-header'] = mail
    # cookie
    res.set_cookie('token', token)
    return res, 200

