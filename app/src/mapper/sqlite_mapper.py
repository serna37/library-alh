import os
import glob
import src
from pathlib import Path
import datetime
import sqlite3
import pandas
from flask import g
#from src import app

# TODO REFACTOR, ORGANIZE

#DATABASE = os.environ.get('DATABASE', '')

def _get_db():
    """Open connection
    """
    con = sqlite3.connect(os.environ.get('DATABASE', ''))
    #db = getattr(g, '_database', None)
    #if db is None:
    #    db = g._database = sqlite3.connect(DATABASE)
    return con

#@app.teardown_appcontext
def _close_connection(_):
    """Close connection
    """
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def _read(func, *args):
    """read & close
    """
    con = _get_db()
    res = func(con, *args)
    con.close()
    return res

def _exe(func, *args):
    """execute & commit
    """
    con = _get_db()
    res = func(con, *args)
    con.commit()
    con.close()
    return res, con

def create_all():
    """CREATE by DDL
    """
    _exe(_create_all)

def _create_all(con):
    ddl_path = Path(__file__).resolve().parent.joinpath('../../ddl')
    ddls = glob.glob(f'{ddl_path}/*.sql')
    for ddl in ddls:
        with open(ddl, 'r', encoding='utf-8') as f:
            query = f.read()
            con.execute(query)

def select(query, data_json):
    """SELECT as DataFrame
    """
    return _read(_select, query, data_json)

def _select(con, query, data_json):
    c = con.cursor()
    q = c.execute(query, data_json)
    cols = [column[0] for column in q.description]
    results = pandas.DataFrame.from_records(data=q.fetchall(), columns=cols)
    c.close()
    return results
    #df = pandas.read_sql_query(sql=query, con=con)
    #return df.to_json(orient='records')

def insert(query, data_json):
    """INSERT
    """
    _exe(_insert, query, data_json)

def _insert(con, query, data_json):
    con.execute(query, data_json)
    #df = pandas.read_sql_query(sql=f'SELECT * FROM {table} LIMIT 1', con=con)
    #df_data = pandas.DataFrame(data=data, columns=df.columns)
    #df_data.to_sql(name=table, con=con, if_exists='append', index=False)

def df_insert(table, df_json):
    _exe(_df_insert, table, df_json)

def _df_insert(con, table, df_json):
    pandas.DataFrame(df_json).to_sql(table, con, if_exists='append', index=False)

# TODO
def upsert(con, data, table, select_1):
    df = pandas.read_sql_query(sql=select_1, con=con)
    df_ins = pandas.DataFrame(data=data, columns=df.columns)
    df_ins.to_sql(name=table, con=con, if_exists='replace', index=False)




#db = f'data.db'
#create_table = f'CREATE TABLE IF NOT EXISTS bookmarks (tweetid, category, created_at, updated_at);'
#create_index = f'CREATE INDEX IF NOT EXISTS idx_bookmarks_01 ON bookmarks(tweetid);'

select_1 = f'SELECT * FROM bookmarks LIMIT 1;'
select_all = f'SELECT * FROM bookmarks;'
select_uncategorised = f'SELECT * FROM bookmarks WHERE category IS NULL;'
select_ = f"""
SELECT
    rowid,
    tweetid,
    category
FROM
    bookmarks
ORDER BY
    RANDOM()
LIMIT
"""

# TODO


#def create():
#    #con = sqlite3.connect(db)
#    #cur = con.cursor()
#    #cur.execute(create_table)
#    #cur.execute(create_index)
#    #con.close()
#
#
#def delins(data):
#    if not isinstance(data, list) or not data:
#        return
#    #con = sqlite3.connect(db)
#    # bulk insert
#    now = datetime.datetime.now()
#    arr_2d = [[v, None, now, now] for v in data]
#    df = pandas.read_sql_query(sql=select_1, con=con)
#    df_ins = pandas.DataFrame(data=arr_2d, columns=df.columns)
#    df_ins.to_sql(name='bookmarks', con=con, if_exists='replace', index=False)
#    con.close()

