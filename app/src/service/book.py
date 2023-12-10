from src.mapper import sqlite_mapper as sql
import json

def addpublisher(data):
    # unique cd, name
    df1 = sql.select('SELECT COUNT(id) FROM mst_books_publisher WHERE publisher_cd = :cd', dict(cd=data['publisher_cd']))
    if df1.iat[0, 0] != 0:
        return {'code': 20, 'status': 'error', 'msg': 'publisher code duplicated.'}

    df2 = sql.select('SELECT COUNT(id) FROM mst_books_publisher WHERE publisher_name = :nm', dict(nm=data['publisher_name']))
    if df2.iat[0, 0] != 0:
        return {'code': 20, 'status': 'error', 'msg': 'publisher name duplicated.'}

    # insert
    sql.insert('mst_books_publisher', [data])
    return {'code': 0, 'status': 'success', 'msg': 'publisher confirmed.'}

def search(data):
    limit = 3
    offset = data['offset']
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
        GROUP BY mb.id
        LIMIT :limit OFFSET :offset
        '''
    df = sql.select(query, dict(limit=limit, offset=offset))
    ans = df.to_json(orient='records')
    obj = json.loads(ans) # if empty, ans is string "[]"
    return {'code': 0, 'status': 'success', 'msg': 'searched.', 'data': obj}

