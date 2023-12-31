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
    LEFT JOIN trn_action_history history ON tu.id = history.user_id
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


# TODO under this, DELETE


def addpublisher(data):
    # unique cd, name
    df1 = sql.select(
        'SELECT COUNT(id) FROM mst_books_publisher WHERE publisher_cd = :cd',
        dict(cd=data['publisher_cd']))
    if df1.iat[0, 0] != 0:
        return {
            'code': 20,
            'status': 'error',
            'msg': 'publisher code duplicated.'
        }

    df2 = sql.select(
        'SELECT COUNT(id) FROM mst_books_publisher WHERE publisher_name = :nm',
        dict(nm=data['publisher_name']))
    if df2.iat[0, 0] != 0:
        return {
            'code': 20,
            'status': 'error',
            'msg': 'publisher name duplicated.'
        }

    # insert
    sql.insert('mst_books_publisher', [data])
    return {'code': 0, 'status': 'success', 'msg': 'publisher confirmed.'}


def search(data):
    limit = 3
    args = dict(limit=limit, offset=data['offset'])
    query = '''
        SELECT
            mb.id
            ,mb.book_name
            ,mb.author_name
            ,mbp.publisher_name
            ,mb.published_at
            ,mbi.img book_img
            ,mbp.img publisher_img
            ,GROUP_CONCAT(ma.attribute) attr
        FROM mst_books mb
        INNER JOIN mst_books_publisher mbp ON mb.publisher_cd = mbp.publisher_cd
        INNER JOIN mst_books_img mbi ON mb.id = mbi.book_id
        INNER JOIN mst_book_attr mba ON mb.id = mba.book_id
        INNER JOIN mst_attributes ma ON mba.attribute_id = ma.attribute_id
        WHERE 1 = 1
    '''

    if data['book_name']:
        query += ' AND mb.book_name like :book_name'
        args['book_name'] = '%' + data['book_name'] + '%'

    if data['author_name']:
        query += ' AND mb.author_name like :author_name'
        args['author_name'] = '%' + data['author_name'] + '%'

    if data['publisher_name']:
        query += ' AND mbp.publisher_name like :publisher_name'
        args['publisher_name'] = '%' + data['publisher_name'] + '%'

    if data['published_from']:
        query += ' AND mb.published_at >= :published_from'
        args['published_from'] = data['published_from']

    if data['published_to']:
        query += ' AND mb.published_at <= :published_to'
        args['published_to'] = data['published_to']

    query += '''
        GROUP BY mb.id
        LIMIT :limit OFFSET :offset
        '''

    df = sql.select(query, args)
    ans = df.to_json(orient='records')
    obj = json.loads(ans)  # if empty, ans is string "[]"
    return {'code': 0, 'status': 'success', 'msg': 'searched.', 'data': obj}
