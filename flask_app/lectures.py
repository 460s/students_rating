from flask import (Blueprint, g, redirect, render_template, request, url_for)
from flask_app.server import login_required
from flask_app.db import get_db

bp = Blueprint('lectures', __name__, )


def user_lectures():
    db = get_db()
    if request.method == 'POST':
        if 'lecture' in request.form:
            lecture_id = request.form['lecture']
            db.execute('INSERT INTO t2u (task, user) VALUES (?, ?)', (lecture_id, g.user["id"]))
            db.commit()
        return redirect(url_for('lectures.lectures'))
    else:
        lectures_list = db.execute(
            'SELECT t.id, t.name, t.description, t2u.user, t2u.grade, t.pass_from, t.pass_to, '
            ' CASE WHEN current_timestamp >= datetime(pass_from, \'unixepoch\') AND '
            'current_timestamp <= datetime(pass_to, \'unixepoch\') THEN 1 ELSE 0 END AS available '
            'FROM task t '
            'LEFT JOIN t2u ON t2u.task = t.id AND t2u.user = ? '
            'GROUP BY t.id', (g.user["id"],)
        ).fetchall()
        return render_template('other/lectures.html', lectures=lectures_list)


def admin_lestures():
    return redirect(url_for('user.userlist'))


@bp.route('/lectures', methods=('GET', 'POST'))
@login_required
def lectures():
    if g.user["admin"] == 1:
        return admin_lestures()
    else:
        return user_lectures()
