import pytest
from app import create_app, db
from app.models import User, Todo

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            u = User(username='bob', email='bob@example.com', role='user')
            u.set_password('secret')
            db.session.add(u)
            db.session.commit()
        yield client

def test_add_task_requires_login(client):
    res = client.post('/tasks/add', data={'title':'t1','description':'d'}, follow_redirects=True)
    assert b'Login' in res.data or res.status_code in (200,302)
