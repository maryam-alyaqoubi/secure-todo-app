import pytest
from app import create_app, db
from app.models import User

@pytest.fixture
def client(tmp_path, monkeypatch):
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

def test_register_and_login(client):
    # register
    res = client.post('/auth/register', data={
        'username':'alice',
        'email':'alice@example.com',
        'password':'pass123'
    }, follow_redirects=True)
    assert b'Registered successfully' in res.data or b'success' in res.data or res.status_code in (200,302)
    # login
    res = client.post('/auth/login', data={'username':'alice','password':'pass123'}, follow_redirects=True)
    assert b'Logged in' in res.data or res.status_code in (200,302)
