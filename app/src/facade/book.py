from src import app
from src.vital import core
from flask import request, jsonify
from src.service import book as service

# ===============
# addpublisher
# ===============
addpub_schema = {
    'publisher_cd': {
        'type': 'string',
        'required': True,
        'empty': False,
        'maxlength': 50
    },
    'publisher_name': {
        'type': 'string',
        'required': True,
        'empty': False,
        'maxlength': 50
    },
    'img': {
        'type': 'string',
        'required': True,
        'empty': False
    }
}


@app.route('/book/addpublisher', methods=['POST'])
@core.authentication()
@core.validation(addpub_schema)
def donation():
    res = service.addpublisher(request.json)
    return jsonify(res), 200


# ===============
# getpublishers
# ===============

# ===============
# getocr
# ===============

# ===============
# donation
# ===============

# ===============
# search
# ===============
search_schema = {
    'offset': {
        'type': 'integer',
        'required': True
    },
    'book_name': {
        'type': 'string',
        'required': False,
        'empty': True,
        'maxlength': 255
    },
    'author_name': {
        'type': 'string',
        'required': False,
        'empty': True,
        'maxlength': 255
    },
    'publisher_name': {
        'type': 'string',
        'required': False,
        'empty': True,
        'maxlength': 255
    },
    'published_from': {
        'type': 'string',
        'required': False,
        'empty': True,
        'maxlength': 255
    },
    'published_to': {
        'type': 'string',
        'required': False,
        'empty': True,
        'maxlength': 255
    }
}


@app.route('/book/search', methods=['POST'])
@core.validation(search_schema)
def search():
    res = service.search(request.json)
    return jsonify(res), 200


# ===============
# detail
# ===============
detail_schema = {'book_id': {'required': True}}


@app.route('/book/detail', methods=['POST'])
@core.validation(detail_schema)
def detail():
    user_id = request.headers.get('x-auth-header', '')
    res = service.get_detail(user_id, request.json)
    return jsonify(res), 200
