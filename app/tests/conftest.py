import os
import pytest
import src
from src.mapper import sqlite_mapper as sql

@pytest.fixture(scope='session')
def client():
    src.app.config['TESTING'] = True
    os.environ['DATABASE'] = 'app/test.db'
    os.environ['DML'] = '../../dml-test'

    print('=========== Initiate DB ===========')
    print('Truncate TestDB File')
    os.remove('app/test.db')
    print('Apply DDL')
    sql.create_all()
    print('Apply Test DML')
    sql.munpilate_all()
    print('=========== Prepared. ===========')

    print('=========== START TEST ===========')
    with src.app.test_client() as client:
        with src.app.app_context():
            yield client

    print('=========== END TEST ===========')

