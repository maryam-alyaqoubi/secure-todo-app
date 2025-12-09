from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from .models import User
from . import db
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import gen_salt
import re

auth_bp = Blueprint('auth', __name__)

# Toggle value: start with vulnerable demonstration turned OFF by default here.
# We will demonstrate vulnerabilities by temporarily editing this to True before the "vulnerable commit".
USE_VULN = False

def is_valid_username(u):
    return re.fullmatch(r'[A-Za-z0-9_.-]{3,30}', u) is not None

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username','').strip()
        email = request.form.get('email','').strip()
        password = request.form.get('password','').strip()

        # Basic server-side validation (fixed)
        if not username or not email or not password:
            flash('All fields are required', 'error')
            return redirect(url_for('auth.register'))
        if not is_valid_username(username):
            flash('Invalid username - use 3-30 chars: letters, numbers, ._-', 'error')
            return redirect(url_for('auth.register'))

        if USE_VULN:
            # VULNERABLE: naive insertion using raw SQL and storing plain password
            # This block is intentionally vulnerable for demonstration. Do not use in production.
            from flask import current_app
            engine = db.get_engine(current_app)
            conn = engine.connect()
            raw_q = f"INSERT INTO users (username, email, password_hash, role) VALUES ('{username}','{email}','{password}','user')"
            conn.execute(raw_q)
            conn.close()
        else:
            # Secure: hash password and use ORM
            if User.query.filter((User.username==username)|(User.email==email)).first():
                flash('User or email already exists', 'error')
                return redirect(url_for('auth.register'))
            u = User(username=username, email=email, role='user')
            u.set_password(password)
            db.session.add(u)
            db.session.commit()
            flash('Registered successfully', 'success')
            return redirect(url_for('auth.login'))
    template = 'register_vuln.html' if USE_VULN else 'register_fixed.html'
    return render_template(template)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username','').strip()
        password = request.form.get('password','').strip()
        if USE_VULN:
            # VULN: raw SQL query vulnerable to SQLi
            from flask import current_app
            engine = db.get_engine(current_app)
            conn = engine.connect()
            raw_q = f"SELECT * FROM users WHERE username = '{username}'"
            res = conn.execute(raw_q).first()
            conn.close()
            if res and res['password_hash'] == password:
                # naive session
                session['user_id'] = res['id']
                session['username'] = res['username']
                flash('Logged in (vuln)', 'success')
                return redirect(url_for('todo.index'))
            else:
                flash('Invalid credentials', 'error')
                return redirect(url_for('auth.login'))
        else:
            user = User.query.filter_by(username=username).first()
            if user and user.check_password(password):
                login_user(user)
                flash('Logged in successfully', 'success')
                return redirect(url_for('todo.index'))
            flash('Invalid credentials', 'error')
            return redirect(url_for('auth.login'))
    template = 'login_vuln.html' if USE_VULN else 'login_fixed.html'
    return render_template(template)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out', 'info')
    return redirect(url_for('auth.login'))
