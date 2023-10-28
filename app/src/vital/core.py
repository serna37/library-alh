import functools
from cerberus import Validator
from cerberus.errors import BasicErrorHandler
from flask import request, jsonify
from src.mapper import sqlite_mapper as sql

def authentication():
    """
    common authentication decorator
    """
    def auth(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            token = request.cookies.get('token')
            print(f"token : {token}")
            header = request.headers.get('x-auth-header')
            print(f"header : {header}")
            # TODO DBみる。useridをヘッダで受け取り、cookieの値とtokenが同じでOK
            print('===== come to auth util =====')
            if not request.headers.get('x-auth-header') == 'alh03test55book':
                print('auth NG')
                return jsonify('error'), 400
            return func(*args, **kwargs)
        wrapper.__name__ = func.__name__
        return wrapper
    return auth

class CustomErrorHandler(BasicErrorHandler):
    """ OVER WRITE BasicErrorHandler.message """
    def __init__(self, tree=None):
        super(CustomErrorHandler, self).__init__(tree)
        # override
        self.messages = {
            0x00: "{0}",
            0x01: "document is missing",
            0x02: "required field",
            0x03: "unknown field",
            0x04: "field '{0}' is required",
            0x05: "depends on these values: {constraint}",
            0x06: "{0} must not be present with '{field}'",
            0x21: "'{0}' is not a document, must be a dict",
            0x22: "empty values not allowed",
            0x23: "null value not allowed",
            0x24: "must be one of these types: {constraint}",
            0x26: "length of list should be {0}, it is {1}",
            0x27: "min length is {constraint}",
            0x28: "max length is {constraint}",
            #0x41: "value does not match regex '{constraint}'",
            0x41: "invalid format",
            0x42: "min value is {constraint}",
            0x43: "max value is {constraint}",
            0x44: "unallowed value {value}",
            0x45: "unallowed values {0}",
            0x46: "unallowed value {value}",
            0x47: "unallowed values {0}",
            0x48: "missing members {0}",
            0x61: "field '{field}' cannot be coerced: {0}",
            0x62: "field '{field}' cannot be renamed: {0}",
            0x63: "field is read-only",
            0x64: "default value for '{field}' cannot be set: {0}",
            0x81: "mapping doesn't validate subschema: {0}",
            0x82: "one or more sequence-items don't validate: {0}",
            0x83: "one or more keys of a mapping  don't validate: {0}",
            0x84: "one or more values in a mapping don't validate: {0}",
            0x85: "one or more sequence-items don't validate: {0}",
            0x91: "one or more definitions validate",
            0x92: "none or more than one rule validate",
            0x93: "no definitions validate",
            0x94: "one or more definitions don't validate",
        }

def validation(schema):
    """
    common validation decorator
    """
    def _validation(func):
        def wrapper(*args, **kwargs):
            # XXX pyright can not recognize cerberus
            v = Validator(schema, error_handler=CustomErrorHandler())
            chk = (v.validate(request.json), v.errors)
            if not chk[0]:
                res = {'emsg': chk[1]}
                return jsonify(res), 400
            return func(*args, **kwargs)
        wrapper.__name__ = func.__name__
        return wrapper
    return _validation

