import pytest
from src.mapper import sqlite_mapper as sql

class TestBook:

    # =========================
    # add publisher
    # =========================
    SIGNUP = dict(user_name='test', mail_address='addpublisher@example.com', password='test-password')
    @pytest.fixture()
    def pre_signup(self, client):
        """ PRE FUNCTION """
        return client.post('/sign/up', json=self.SIGNUP)

    def add_publisher(self, client, cd, name, img):
        """ CALL FUNCTION """
        mail = self.SIGNUP['mail_address']
        df = sql.select('SELECT token FROM trn_users WHERE mail_address = :mail', dict(mail=mail))
        client.set_cookie('localhost', 'token', df.iat[0, 0])
        return client.post('/book/addpublisher', json=dict(publisher_cd=cd, publisher_name=name, img=img), headers={'x-auth-header': mail})

    # ================================================================================
    EMG_NULL = 'null value not allowed'
    EMG_EMPTY = 'empty values not allowed'
    EMG_MAX = 'max length is '
    CHAR_51 = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'

    invalided_addpublisher = (
        ('None', None, None, None, {'emsg': {'publisher_cd': [EMG_NULL], 'publisher_name': [EMG_NULL], 'img': [EMG_NULL]}})
        , ('Empty', '', '', '', {'emsg': {'publisher_cd': [EMG_EMPTY], 'publisher_name': [EMG_EMPTY], 'img': [EMG_EMPTY]}})
        , ('MaxLen-Type', CHAR_51, CHAR_51, CHAR_51, {'emsg': {'publisher_cd': [EMG_MAX+'50'], 'publisher_name': [EMG_MAX+'50']}})
    )
    # ================================================================================

    @pytest.mark.usefixtures('pre_signup')
    @pytest.mark.parametrize(['case', 'cd', 'name', 'img', 'res'], invalided_addpublisher ,
                             ids=['VALID_CASE_{}-{}'.format(i, v[0]) for i, v in enumerate(invalided_addpublisher )])
    def test_addpublisher_invalid(self, client, case, cd, name, img, res):
        """ VALIDATOIN """
        _ = case
        rv = self.add_publisher(client, cd, name, img)
        assert res == rv.json
        assert 400 == rv.status_code

    ADD = dict(publisher_cd='publisher_cd_1', publisher_name='publisher_name_1', img='base64_data_string')
    @pytest.mark.usefixtures('pre_signup')
    def test_add_publisher_success(self, client):
        """ SUCCESS """
        rv = self.add_publisher(client, self.ADD['publisher_cd'], self.ADD['publisher_name'], self.ADD['img'])
        assert 200 == rv.status_code
        assert rv.json == {'code': 0, 'status': 'success', 'msg': 'publisher confirmed.'}

    @pytest.mark.usefixtures('pre_signup')
    def test_addpublisher_dup_cd(self, client):
        """ ABNORMAL """
        rv = self.add_publisher(client, self.ADD['publisher_cd'], self.ADD['publisher_name'], self.ADD['img'])
        assert 200 == rv.status_code
        assert rv.json == {'code': 20, 'status': 'error', 'msg': 'publisher code duplicated.'}

    @pytest.mark.usefixtures('pre_signup')
    def test_addpublisher_dup_nm(self, client):
        """ ABNORMAL """
        rv = self.add_publisher(client, self.ADD['publisher_cd']+'_', self.ADD['publisher_name'], self.ADD['img'])
        assert 200 == rv.status_code
        assert rv.json == {'code': 20, 'status': 'error', 'msg': 'publisher name duplicated.'}


