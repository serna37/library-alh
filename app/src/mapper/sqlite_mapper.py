import os
import glob
from pathlib import Path
from os.path import split
import sqlite3
import pandas

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

def munpilate_all():
    """Apply DML
    """
    _exe(_dml)

def _dml(con):
    pt = os.environ.get('DML', '')
    dml_path = Path(__file__).resolve().parent.joinpath(pt)
    dmls = glob.glob(f'{dml_path}/*.csv')
    for dml in dmls:
        table_name = split(dml)[1][0:-4]
        df = pandas.read_csv(dml, dtype=object)
        df.to_sql(table_name, con=con, if_exists="append", index=False)

def select(query, data_json):
    """SELECT as DataFrame
    :param string SQL query
    :param json Binding Parameters JSON
    :return DataFrame
    """
    return _read(_select, query, data_json)

def _select(con, query, data_json):
    c = con.cursor()
    q = c.execute(query, data_json)
    cols = [column[0] for column in q.description]
    results = pandas.DataFrame.from_records(data=q.fetchall(), columns=cols)
    c.close()
    return results

def insert(table, df_json):
    """INSERT DataFrame
    :param string Table Name
    :param json DataFrame JSON such as [{'columname': 'value'}]
    """
    _exe(_insert, table, df_json)

def _insert(con, table, df_json):
    pandas.DataFrame(df_json).to_sql(table, con, if_exists='append', index=False)

def _get_db():
    """Open connection
    """
    con = sqlite3.connect(os.environ.get('DATABASE', ''))
    return con

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



#def insert(query, data_json):
#    """INSERT
#    """
#    _exe(_insert, query, data_json)
#
#def _insert(con, query, data_json):
#    con.execute(query, data_json)
#    #df = pandas.read_sql_query(sql=f'SELECT * FROM {table} LIMIT 1', con=con)
#    #df_data = pandas.DataFrame(data=data, columns=df.columns)
#    #df_data.to_sql(name=table, con=con, if_exists='append', index=False)


#def upsert(con, data, table, select_1):
#    df = pandas.read_sql_query(sql=select_1, con=con)
#    df_ins = pandas.DataFrame(data=data, columns=df.columns)
#    df_ins.to_sql(name=table, con=con, if_exists='replace', index=False)

