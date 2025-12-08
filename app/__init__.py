from flask import Flask
from .models import init_db

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev-secret-key'  # replace with env var in production
    init_db()
    from .auth import auth_bp
    from .todo import todo_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(todo_bp)
    return app

# If running directly
if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
