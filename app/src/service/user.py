from src.mapper import sqlite_mapper as sql
import json


def get_user_profile(user_id):
    query = '''
    SELECT
        tu.user_name
        , tu.mail_address
        , book.book_name
        , book.author_name
        , history.action
        , history.num
    FROM trn_users tu
    LEFT JOIN trn_action_history history ON tu.mail_address = history.user_id
    LEFT JOIN mst_books book ON history.book_id = book.id
    WHERE tu.mail_address = :mail
    '''
    df = sql.select(query, dict(mail=user_id))
    ans = df.to_json(orient='records')
    obj = json.loads(ans)  # if empty, ans is string "[]"
    return {
        'code': 0,
        'status': 'success',
        'msg': 'get user progile.',
        'data': obj
    }


def get_rental_state(user_id):
    query = '''
    SELECT
        mb.book_name
        , mb.author_name
        , trs.rent_num
    FROM trn_users tu
    LEFT JOIN trn_rental_state trs ON tu.mail_address = trs.user_id
    LEFT JOIN mst_books mb ON trs.book_id = mb.id
    WHERE tu.mail_address = :mail
    '''
    df = sql.select(query, dict(mail=user_id))
    ans = df.to_json(orient='records')
    obj = json.loads(ans)  # if empty, ans is string "[]"
    return {
        'code': 0,
        'status': 'success',
        'msg': 'get user rental state.',
        'data': obj
    }

