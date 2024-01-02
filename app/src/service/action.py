from src.mapper import sqlite_mapper as sql
import json


def rental(user_id, data):
    entity = {
        'book_id': [str(data['book_id'])],
        'user_id': str(user_id),
        'rent_num': str(data['num'])
    }
    sql.insert('trn_rental_state', entity)

    hist = {
        'user_id': [user_id],
        'book_id': data['book_id'],
        'action': 'rental',
        'num': data['num']
    }
    sql.insert('trn_action_history', hist)
    return {'code': 0, 'status': 'success', 'msg': 'rental.'}


def book_return(user_id, data):
    # delete
    query = '''
    DELETE FROM trn_rental_state WHERE id IN (
        SELECT id FROM trn_rental_state WHERE
        book_id = :book_id
        AND user_id = :user_id
        AND rent_num = :num
        LIMIT 1
    )
    '''
    entity = {
        'book_id': data['book_id'],
        'user_id': user_id,
        'num': data['num']
    }
    sql.delete(query, entity)

    hist = {
        'user_id': [user_id],
        'book_id': data['book_id'],
        'action': 'return',
        'num': data['num']
    }
    sql.insert('trn_action_history', hist)
    return {'code': 0, 'status': 'success', 'msg': 'return.'}
