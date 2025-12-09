from flask import Blueprint, render_template, request, redirect, url_for, flash, session, abort
from flask_login import login_required, current_user
from .models import Todo, User
from . import db

todo_bp = Blueprint('todo', __name__)

# When USE_VULN=True in auth.py, the templates will use the vulnerable variations
from .auth import USE_VULN

@todo_bp.route('/')
@login_required
def index():
    if USE_VULN:
        # For vuln mode, produce list differently if needed (simulate insecure rendering)
        tasks = Todo.query.filter_by(user_id=current_user.id).all()
        return render_template('index_vuln.html', todos=tasks, username=current_user.username)
    else:
        tasks = Todo.query.filter_by(user_id=current_user.id).all()
        return render_template('index_fixed.html', todos=tasks, username=current_user.username)

@todo_bp.route('/add', methods=['POST'])
@login_required
def add_task():
    title = request.form.get('title','').strip()
    description = request.form.get('description','').strip()
    if not title:
        flash('Title required', 'error')
        return redirect(url_for('todo.index'))

    if USE_VULN:
        # VULN: store data as-is (XSS possible) — actual storage uses ORM but template renders unescaped
        t = Todo(title=title, description=description, user_id=current_user.id)
        db.session.add(t)
        db.session.commit()
    else:
        # Secure: validate lengths and escape at render time
        if len(title) > 255:
            flash('Title too long', 'error')
            return redirect(url_for('todo.index'))
        t = Todo(title=title, description=description, user_id=current_user.id)
        db.session.add(t)
        db.session.commit()
    flash('Task added', 'success')
    return redirect(url_for('todo.index'))

@todo_bp.route('/complete/<int:task_id>', methods=['POST'])
@login_required
def complete_task(task_id):
    task = Todo.query.get_or_404(task_id)
    if task.user_id != current_user.id and current_user.role != 'admin':
        abort(403)
    task.completed = True
    db.session.commit()
    flash('Task marked complete', 'success')
    return redirect(url_for('todo.index'))

@todo_bp.route('/delete/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Todo.query.get_or_404(task_id)
    if task.user_id != current_user.id and current_user.role != 'admin':
        abort(403)
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted', 'info')
    return redirect(url_for('todo.index'))
