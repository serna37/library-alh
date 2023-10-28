import os
import base64
from src.service import sign

def test_signup_hash_password_same():
    salt = base64.b64encode(os.urandom(32)) 
    plain = 'test-password1'
    rv1 = sign._hash_password(plain, salt)
    rv2 = sign._hash_password(plain, salt)
    assert rv1 == rv2

def test_signup_hash_password_reverse():
    salt = base64.b64encode(os.urandom(32)) 
    plain = 'test-password2'
    password = sign._hash_password(plain, salt)
    rv = sign._hash_check(plain, password)
    assert rv == True

