import pytest
import src.mapper.sqlite_mapper as sql

class TestSign():

    # =========================
    # sign up
    # =========================
    def signup(self, client, username, mailaddress, password):
        return client.post('/sign/up', json=dict(user_name=username, mail_address=mailaddress, password=password))

    OK_REQ = ('test', 'test@example.com', 'test-password')

    EMG_NULL = 'null value not allowed'
    EMG_EMPTY = 'empty values not allowed'
    EMG_MIN = 'min length is '
    EMG_MAX = 'max length is '
    EMG_FMT = 'invalid format'

    CHAR_201 = 'a@aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'

    invalided_signup = (
        ('None', None, None, None, {'emsg': {'user_name': [EMG_NULL], 'mail_address': [EMG_NULL], 'password': [EMG_NULL]}})
        , ('Empty', '', '', '', {'emsg': {'user_name': [EMG_EMPTY], 'mail_address': [EMG_EMPTY], 'password': [EMG_MIN+'8']}})
        , ('MinLen', 'a', 'a', 'a', {'emsg': {'mail_address': [EMG_FMT], 'password': [EMG_MIN+'8']}})
        , ('MaxLen', CHAR_201, CHAR_201, CHAR_201, {'emsg': {'user_name': [EMG_MAX+'200'], 'mail_address': [EMG_MAX+'200'], 'password': [EMG_MAX+'200']}})
        , ('Type', 'test', 'dummy', 'test-password', {'emsg': {'mail_address': [EMG_FMT]}})
    )

    @pytest.mark.parametrize(['case', 'username', 'mailaddress', 'password', 'res'], invalided_signup,
                             ids=['VALID_CASE_{}-{}'.format(i, v[0]) for i, v in enumerate(invalided_signup)])
    def test_signup_valid(self, case, client, username, mailaddress, password, res):
        _ = case
        rv = self.signup(client, username, mailaddress, password)
        assert res == rv.json
        assert 400 == rv.status_code

    def test_signup_success(self, client):
        rv = self.signup(client, *self.OK_REQ)
        df = sql.select('SELECT * FROM trn_users WHERE mail_address = :str', {'str': self.OK_REQ[1]})
        assert 200 == rv.status_code
        assert rv.json == {'code': 0, 'status': 'success', 'msg': 'sign up success.'}
        assert rv.headers['x-auth-header'] == self.OK_REQ[1]
        assert 'token=' in rv.headers['Set-Cookie']
        assert df.loc[0, 'user_name'] == self.OK_REQ[0]
        assert df.loc[0, 'mail_address'] == self.OK_REQ[1]

    def test_signup_dupl_mail_address(self, client):
        rv = self.signup(client, *self.OK_REQ)
        assert 200 == rv.status_code
        assert rv.json == {'code': 20, 'status': 'error', 'msg': 'mail address duplicated.'}
        assert rv.headers['x-auth-header'] == ''
        assert rv.headers['Set-Cookie'] == 'token=; Path=/'


    # =========================
    # sign in
    # =========================
    def signin(self, client, mail_address, password):
        return client.post('/sign/in', json=dict(mail_address=mail_address, password=password))

    OK_REQ2 = ('test', 'test2@example.com', 'test-password')

    @pytest.fixture()
    def pre_signin(self, client):
        return client.post('/sign/up', json=dict(user_name=self.OK_REQ2[0], mail_address=self.OK_REQ2[1], password=self.OK_REQ2[2]))

    invalided_signin = (
        ('None', None, None, {'emsg': {'mail_address': [EMG_NULL], 'password': [EMG_NULL]}})
        , ('Empty', '', '', {'code': 20, 'status': 'error', 'msg': 'access denied.'})
    )
    @pytest.mark.parametrize(['case', 'mailaddress', 'password', 'res'], invalided_signin,
                             ids=['VALID_CASE_{}-{}'.format(i, v[0]) for i, v in enumerate(invalided_signin)])
    def test_signin_valid(self, case, client, mailaddress, password, res):
        rv = self.signin(client, mailaddress, password)
        assert res == rv.json
        if case == 'None':
            assert 400 == rv.status_code
        if case == 'Empty':
            assert 200 == rv.status_code

    def test_signin_miss_no_mail(self, client):
        rv = self.signin(client, 'no-exists-mail', 'pass')
        assert rv.status_code == 200
        assert rv.json == {'code': 20, 'status': 'error', 'msg': 'access denied.'}
        assert rv.headers['x-auth-header'] == ''
        assert rv.headers['Set-Cookie'] == 'token=; Path=/'

    @pytest.mark.usefixtures('pre_signin')
    def test_signin_miss_no_match(self, client):
        rv = self.signin(client, self.OK_REQ2[1], 'miss-password')
        assert rv.status_code == 200
        assert rv.json == {'code': 20, 'status': 'error', 'msg': 'access denied.'}
        assert rv.headers['x-auth-header'] == ''
        assert rv.headers['Set-Cookie'] == 'token=; Path=/'

    @pytest.mark.usefixtures('pre_signin')
    def test_signin_success(self, client):
        rv = self.signin(client, self.OK_REQ2[1], self.OK_REQ2[2])
        assert rv.status_code == 200
        assert rv.json == {'code': 0, 'status': 'success', 'msg': 'sign in success.'}
        assert rv.headers['x-auth-header'] == self.OK_REQ2[1]
        assert 'token=' in rv.headers['Set-Cookie']

