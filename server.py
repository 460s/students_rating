import functools
from db import get_db
from flask import (
    render_template, flash, g, request, Blueprint, redirect, url_for, session )
from werkzeug.security import check_password_hash, generate_password_hash
from flask_simplelogin import SimpleLogin
bp = Blueprint('server', __name__,)

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
#@login_required
def index():
    return render_template('index.html')

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
            error = 'Password is required.'
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

@bp.route('/lectures')
@login_required
def lectures():
    return render_template('other/lectures.html')
