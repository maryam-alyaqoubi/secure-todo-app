from flask import Blueprint, request, render_template, redirect, url_for, session, flash
from .models import create_user_vuln, get_user_vuln, create_user_secure, get_user_secure

auth_bp = Blueprint('auth', __name__)

# Choose which functions to import/use later by editing these aliases
USE_SECURE = False  # set True in fixed branch/commit

@auth_bp.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if USE_SECURE:
            create_user_secure(username, password)
        else:
            create_user_vuln(username, password)
        flash('Registered successfully')
        return redirect(url_for('auth.login'))
    # show different templates for vuln vs fixed to demo XSS differences
    template = 'register_fixed.html' if USE_SECURE else 'register_vuln.html'
    return render_template(template)

@auth_bp.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = get_user_secure(username) if USE_SECURE else get_user_vuln(username)
        if not user:
            flash('Invalid credentials')
            return redirect(url_for('auth.login'))
        # password check naive for vuln branch (plain text), hashed for secure
        if USE_SECURE:
            from werkzeug.security import check_password_hash
            if check_password_hash(user[2], password):
                session['user'] = user[1]
                return redirect(url_for('todo.index'))
        else:
            if user[2] == password:
                session['user'] = user[1]
                return redirect(url_for('todo.index'))
        flash('Invalid credentials')
        return redirect(url_for('auth.login'))
    return render_template('register_vuln.html')
