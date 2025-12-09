from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import os

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__, static_folder="../static", template_folder="templates")
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-me')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Mony%40512@localhost/secure_todo_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # session cookie settings
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    # in production set SESSION_COOKIE_SECURE = True

    # init extensions
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # register blueprints
    from .auth import auth_bp
    from .todo import todo_bp
    from .admin import admin_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(todo_bp, url_prefix='/tasks')
    app.register_blueprint(admin_bp, url_prefix='/admin')

    # setup user_loader for Flask-Login
    from .models import User  # تأكدي أن models.py فيه User class
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # create DB schema if missing
    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            print("Warning: db.create_all() failed:", e)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
