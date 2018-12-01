import functools
import os

from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash

from flask_app.db import get_db

bp = Blueprint('server', __name__, )


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('server.login'))

        return view(**kwargs)

    return wrapped_view


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


@bp.route('/')
# @login_required
def index():
    limit = int(os.environ.get('RATING_LIST_MAX_ELEMENTS', 5))
    db = get_db()
    students = db.execute(
        'SELECT u.username, IFNULL(SUM(t2u.grade), 0) grade '
        'FROM user u '
        'LEFT JOIN  t2u ON u.id = t2u.user '
        'GROUP BY u.username '
        'ORDER BY grade DESC, SUM(t2u.id)').fetchall()
    students = [s for i, s in enumerate(students) if
                g.user is not None and s["username"] == g.user["username"] or i < limit and s["grade"] != 0]

    return render_template('index.html', students=students, limit=limit)


@bp.route('/reg', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        repository = request.form['repository']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif not repository:
            error = 'Repository is required.'
        elif db.execute(
                'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {0} is already registered.'.format(username)

        if error is None:
            db.execute(
                'INSERT INTO user (username, password, repository) VALUES (?, ?, ?)',
                (username, generate_password_hash(password), repository)
            )
            db.commit()
            return redirect(url_for('server.login'))

        flash(error)

    return render_template("auth/register.html")


@bp.route('/log', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('server.index'))

        flash(error)

    return render_template('auth/login.html')


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('server.index'))
