import pytest
from src.mapper import sqlite_mapper as sql

class TestAuth:

    # =========================
    # sign up
    # =========================

    def ping(self, client, header):
        return client.get('/ping', headers={'x-auth-header': header})

    OK_REQ = ('test', 'authtest@example.com', 'test-password')

    @pytest.fixture()
    def pre(self, client):
        return client.post('/sign/up', json=dict(user_name=self.OK_REQ[0], mail_address=self.OK_REQ[1], password=self.OK_REQ[2]))

    @pytest.mark.usefixtures('pre')
    def test_auth_no_header_cookie(self, client):
        rv = client.get('/ping')
        assert rv.status_code == 401
        assert 'unauthorized' == rv.json

    def test_auth_miss(self, client):
        df = sql.select('SELECT token FROM trn_users WHERE mail_address = :mail', dict(mail=self.OK_REQ[1]))
        client.set_cookie('localhost', 'token', df.iat[0, 0] + 'dummy')
        rv = self.ping(client, self.OK_REQ[1] + 'dummy')
        assert rv.status_code == 401
        assert 'unauthorized' == rv.json

    def test_auth_success(self, client):
        df = sql.select('SELECT token FROM trn_users WHERE mail_address = :mail', dict(mail=self.OK_REQ[1]))
        client.set_cookie('localhost', 'token', df.iat[0, 0])
        rv = self.ping(client, self.OK_REQ[1])
        assert rv.status_code == 200
        assert 'ok' == rv.json

