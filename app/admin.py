from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from .models import User, Todo
from . import db

admin_bp = Blueprint('admin', __name__)

def admin_required(fn):
    from functools import wraps
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            abort(403)
        return fn(*args, **kwargs)
    return wrapper

@admin_bp.route('/')
@login_required
@admin_required
def dashboard():
    users = User.query.all()
    tasks = Todo.query.all()
    return render_template('admin_dashboard.html', users=users, tasks=tasks)

@admin_bp.route('/promote/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def promote(user_id):
    u = User.query.get_or_404(user_id)
    u.role = 'admin'
    db.session.commit()
    flash(f'{u.username} promoted to admin', 'success')
    return redirect(url_for('admin.dashboard'))
