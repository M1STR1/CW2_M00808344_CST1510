from app.Application import hash_password, validate_hash

def test_hash_and_validate():
    pwd = "TestPass1!"
    h = hash_password(pwd)
    assert isinstance(h, str)
    assert validate_hash(pwd, h)
    assert not validate_hash("wrong", h)