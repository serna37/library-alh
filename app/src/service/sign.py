import os
import base64
import hashlib
import secrets
from src.mapper import sqlite_mapper as sql

def singup(data):
    # 1. mail address duplicate check
    cnt = sql.select('SELECT COUNT(id) cnt FROM trn_users WHERE mail_address = :mail_address', {'mail_address': data['mail_address']})
    if cnt.iat[0, 0] != 0:
        return {'code': 20, 'status': 'error', 'msg': 'mail address duplicated.'}, '', ''
    # 2. hash password
    data['password'] = _hash_password(data['password'], base64.b64encode(os.urandom(32)))
    # 3. generate token
    token = secrets.token_hex()
    data['token'] = token
    # 4. insert data
    df = [data]
    sql.df_insert(df)
    # 5. return auth info
    return {'code': 0, 'status': 'success', 'msg': 'sign up success.'}, data['mail_address'], token

def signin(data):
    # 1. get salt by mail address
    df = sql.select('SELECT * FROM trn_users WHERE mail_address = :mail_address', {'mail_address': data['mail_address']})
    if df.empty:
        return {'code': 20, 'status': 'error', 'msg': 'access denied.'}, '', ''
    password = df.loc[0, 'password']
    # 2. check hash
    if not _hash_check(data['password'], password):
        return {'code': 20, 'status': 'error', 'msg': 'access denied.'}, '', ''
    # 3. return auth info
    return {'code': 0, 'status': 'success', 'msg': 'sign in success.'}, df.loc[0, 'mail_address'], df.loc[0, 'token']

# ==================================================
# internal functions
# ==================================================
def _hash_password(password, salt):
    # hash with sha256
    pass_byte = bytes(password, 'utf-8')
    digest = hashlib.sha256(salt + pass_byte).hexdigest()
    # stretching
    for _ in range(10000):
        digest = hashlib.sha256(bytes(digest, 'utf-8')).hexdigest()
    # return salt+hash
    salt_str = salt.decode('utf-8')
    return f'{salt_str}$${digest}'

def _hash_check(plain, password):
    salt = password.split('$$')[0]
    digest = _hash_password(plain, bytes(salt, 'utf-8'))
    return password == digest
