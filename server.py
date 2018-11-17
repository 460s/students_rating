from flask import Flask
from db import get_db
from flask import (
    render_template, flash, request, Blueprint, redirect, url_for )
from werkzeug.security import check_password_hash, generate_password_hash
from flask_simplelogin import SimpleLogin
bp = Blueprint('server', __name__,)
# app = Flask(__name__)
# SimpleLogin(app)

@bp.route('/')
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
            return redirect(url_for('simplelogin.login'))

        flash(error)

    return render_template("auth/register.html")


def login_checker(user):
    """:param user: dict {'username': 'foo', 'password': 'bar'}"""
    if user.get('username') == 'chuck' and user.get('password') == 'norris':
       return True  # <--- Allowed
    return False  # <--- Denied


SimpleLogin(bp, login_checker=login_checker)
