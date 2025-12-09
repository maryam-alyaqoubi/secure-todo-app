import pytest
from app import create_app, db
from app.models import User

@pytest.fixture
def app_with_users():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
        admin = User(username='admin',email='a@a.com',role='admin')
        admin.set_password('adminpass')
        user = User(username='user',email='u@u.com',role='user')
        user.set_password('userpass')
        db.session.add_all([admin,user])
        db.session.commit()
    return app

def test_admin_role_present(app_with_users):
    with app_with_users.app_context():
        from app.models import User
        assert User.query.filter_by(role='admin').count() == 1
