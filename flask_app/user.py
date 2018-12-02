from flask import (Blueprint, g, redirect, render_template, request, url_for)
from flask_app.server import admin_required
from flask_app.db import get_db


bp = Blueprint('user', __name__, )


@bp.route('/users', methods=('GET', 'POST'))
@admin_required
def userlist():
    if g.user["admin"] != 1:
        raise Exception('admin access required')

    db = get_db()
    if request.method == 'POST':
        form = request.form.to_dict(flat=False)
        db.execute('UPDATE user SET is_admin = 0')
        if 'admin' in form:
            for value in form['admin']:
                db.execute('UPDATE user SET is_admin = 1 WHERE id = ?', (value,))
        db.commit()
        return redirect(url_for('user.userlist'))
    else:
        users_list = db.execute(
            'SELECT u.id, u.username, u.repository, IFNULL(u.is_admin, 0) AS admin '
            'FROM user u'
        ).fetchall()
        return render_template('other/users.html', users=users_list)
