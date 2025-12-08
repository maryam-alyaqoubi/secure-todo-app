from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from .models import add_todo_vuln, add_todo_secure, list_todos

todo_bp = Blueprint('todo', __name__)

USE_SECURE = False  # set True in fixed branch

@todo_bp.route('/')
def index():
    user = session.get('user')
    if not user:
        return redirect(url_for('auth.login'))
    todos = list_todos(user)
    template = 'index_fixed.html' if USE_SECURE else 'index_vuln.html'
    return render_template(template, todos=todos, username=user)

@todo_bp.route('/add', methods=['POST'])
def add():
    user = session.get('user')
    if not user:
        return redirect(url_for('auth.login'))
    task = request.form.get('task')
    if USE_SECURE:
        add_todo_secure(user, task)
    else:
        add_todo_vuln(user, task)
    flash('Task added')
    return redirect(url_for('todo.index'))
