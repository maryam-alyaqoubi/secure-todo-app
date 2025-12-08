from app.models import init_db, create_user_vuln, get_user_vuln, DB
import os
import sqlite3

def test_create_and_get_user(tmp_path, monkeypatch):
    # Use a temp DB for unit test
    dbfile = tmp_path / "test.db"
    monkeypatch.setattr('app.models.DB', str(dbfile))
    init_db()
    create_user_vuln("alice", "password123")
    user = get_user_vuln("alice")
    assert user is not None
    assert user[1] == "alice"
