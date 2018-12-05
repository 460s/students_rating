from flask import (Blueprint, g, redirect, render_template, request, url_for)
from flask_app.server import admin_required
from flask_app.db import get_db


bp = Blueprint('task', __name__, )


@bp.route('/tasks', methods=('GET', 'POST'))
@admin_required
def tasklist():
    if g.user["admin"] != 1:
        raise Exception('admin access required')

    db = get_db()
    if request.method == 'POST':
        form = request.form.to_dict(flat=True)
        print(form)
        for taskid in form:
            grade = form[taskid]
            db.execute('UPDATE t2u SET grade = ? WHERE id = ?',
                       (grade, taskid))
            db.commit()

        return redirect(url_for('task.tasklist'))
    else:
        task_list = db.execute(
            'SELECT t2u.id, t.name, u.username, u.repository '
            'FROM user u '
            'LEFT JOIN task t '
            'JOIN t2u ON t2u.task = t.id AND t2u.user = u.id '
            'WHERE IFNULL(LENGTH(t2u.grade), 0) = 0 '
            'GROUP BY t2u.id'
        ).fetchall()
        return render_template('other/tasklist.html', tasks=task_list)
