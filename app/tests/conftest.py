import os
import pytest
import src
from src.mapper import sqlite_mapper as sql

@pytest.fixture(scope='session')
def client():
    src.app.config['TESTING'] = True
    os.environ['DATABASE'] = 'app/test.db'

    # drop table
    os.remove('app/test.db')
    # create table by DDL
    sql.create_all()
    # TODO insert test data

    print('=========== START TEST ===========')
    with src.app.test_client() as client:
        with src.app.app_context():
            yield client

    print('=========== END TEST ===========')

