from src.mapper import sqlite_mapper as sql

def addpublisher(data):
    # unique cd, name
    df1 = sql.select('SELECT COUNT(id) FROM mst_books_publisher WHERE publisher_cd = :cd', dict(cd=data['publisher_cd']))
    if df1.iat[0, 0] != 0:
        return {'code': 20, 'status': 'error', 'msg': 'publisher code duplicated.'}

    df2 = sql.select('SELECT COUNT(id) FROM mst_books_publisher WHERE publisher_name = :nm', dict(nm=data['publisher_name']))
    if df2.iat[0, 0] != 0:
        return {'code': 20, 'status': 'error', 'msg': 'publisher name duplicated.'}

    # insert
    sql.df_insert('mst_books_publisher', [data])
    return {'code': 0, 'status': 'success', 'msg': 'publisher confirmed.'}

