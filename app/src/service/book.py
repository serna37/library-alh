from src.mapper import sqlite_mapper as sql
import json


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


def get_detail(user_id, data):
    bid = data['book_id']

    you_rental = 'no'
    if user_id != '':
        is_rental = '''
        SELECT SUM(rent_num) FROM trn_rental_state
        WHERE book_id = :book_id
        AND user_id = :user_id
        '''
        res = sql.select(is_rental, {'book_id': bid, 'user_id': user_id})
        resv = res.iat[0, 0]
        if resv is None:
            resv = 0
        if resv != 0:
            you_rental = 'yes'

    entity = {'book_id': bid}
    get_stock = '''
    SELECT stock FROM mst_books_stock WHERE book_id = :book_id
    '''
    all = sql.select(get_stock, entity)

    get_rentaled = '''
    SELECT SUM(rent_num) FROM trn_rental_state WHERE book_id = :book_id
    '''
    rent = sql.select(get_rentaled, entity)
    rent_num = rent.iat[0, 0]
    if rent_num is None:
        rent_num = 0

    remain = all.iat[0, 0] - rent_num

    comment_query = '''
    SELECT
        tr.comments
        , tu.user_name
    FROM trn_remarks tr
    INNER JOIN trn_users tu ON tr.user_id = tu.mail_address
    AND tr.book_id = :book_id
    AND tr.mark_type = 'comment'
    '''
    com = sql.select(comment_query, entity)
    com_js = com.to_json(orient='records')
    com_obj = json.loads(com_js)  # if empty, ans is string "[]"

    return {'code': 0, 'status': 'success', 'num': str(remain), 'you_rental': you_rental, 'comments': com_obj}
