import time
import os
from pathlib import Path
from app.Application import (
    hash_password, validate_hash,
    _get_lockout, _set_lockout, _reset_lockout,
    _create_session, validate_session, get_session_user, end_session,
    login_user, register_user
)
from tempfile import TemporaryDirectory

def test_lockout_flow(tmp_path):
    # create temp users file and temp lockout file
    users_file = tmp_path / "users.txt"
    lockout_file = tmp_path / "lockouts.json"
    sessions_file = tmp_path / "sessions.json"

    # create a user
    username = "tester"
    pw = "StrongPass123!"
    h = hash_password(pw)
    with open(users_file, "w", encoding="utf-8") as f:
        f.write(f"{username},user,{h}\n")

    # ensure not locked initially
    lock = _get_lockout(username, str(lockout_file))
    assert lock["failed"] == 0 and lock["locked_until"] == 0

    # failed login 1 time, set max_failed to 1 to trigger lockout quickly
    res = login_user(username=username, password="wrongpass", users_file=str(users_file),
                     lockout_file=str(lockout_file), max_failed=1, lockout_seconds=2, sessions_file=str(sessions_file))
    assert res == "invalid"
    # now next attempt should lock
    res2 = login_user(username=username, password="wrongpass", users_file=str(users_file),
                      lockout_file=str(lockout_file), max_failed=1, lockout_seconds=2, sessions_file=str(sessions_file))
    # since max_failed is 1 the first invalid triggers lockout -> second returns "locked"
    assert res2 == "locked"

    # cannot login with correct password while locked
    res3 = login_user(username=username, password=pw, users_file=str(users_file),
                      lockout_file=str(lockout_file), max_failed=1, lockout_seconds=2, sessions_file=str(sessions_file))
    assert res3 == "locked"

    # wait until lockout expires (2 seconds) then login succeeds
    time.sleep(2.1)
    token = login_user(username=username, password=pw, users_file=str(users_file),
                       lockout_file=str(lockout_file), sessions_file=str(sessions_file))
    assert token not in ("locked", "invalid", "notfound")
    assert validate_session(token, str(sessions_file))
    user, role = get_session_user(token, str(sessions_file))
    assert user == username and role == "user"

    # end session
    assert end_session(token, str(sessions_file)) is True
    assert not validate_session(token, str(sessions_file))


def test_create_session_and_validate(tmp_path):
    sessions_file = tmp_path / "sessions.json"
    token = _create_session("bob", "analyst", str(sessions_file), session_seconds=5)
    assert validate_session(token, str(sessions_file))
    user, role = get_session_user(token, str(sessions_file))
    assert user == "bob" and role == "analyst"
    time.sleep(5.1)
    assert not validate_session(token, str(sessions_file))
    # expired -> get_session_user returns None
    u, r = get_session_user(token, str(sessions_file))
    assert u is None and r is None