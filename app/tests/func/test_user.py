import pytest
from src.mapper import sqlite_mapper as sql


class TestUser:

    # =========================
    # get profile
    # =========================

    def call(self, client, header):
        """CALL FUNCTION"""
        return client.post('/user/profile', headers={'x-auth-header': header})

    OK_REQ = ('test', 'authtest@example.com', 'test-password')

    @pytest.fixture()
    def pre(self, client):
        """ PRE SIGN UP """
        return client.post('/sign/up',
                           json=dict(user_name=self.OK_REQ[0],
                                     mail_address=self.OK_REQ[1],
                                     password=self.OK_REQ[2]))

    # depends on data
    def test_get_user_profile_success(self, client):
        """ SUCCESS """
        df = sql.select(
            'SELECT token FROM trn_users WHERE mail_address = :mail',
            dict(mail=self.OK_REQ[1]))
        client.set_cookie('localhost', 'token', df.iat[0, 0])
        rv = self.call(client, self.OK_REQ[1])
        assert rv.status_code == 200
        assert rv.json['code'] == 0
        assert rv.json['msg'] == 'get user progile.'

