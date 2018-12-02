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


@bp.route('/user/tasks', methods=('GET', 'POST'))
@admin_required
def usertasks():
    if g.user["admin"] != 1:
        raise Exception('admin access required')

    db = get_db()
    if request.method == 'POST':
        form = request.form.to_dict(flat=True)
        print(form)
        for taskid in form:
            grade = form[taskid]    
            task2user = db.execute(
                'SELECT * '
                'FROM t2u '
                'WHERE task = ? AND user = ?', (taskid, request.args.get('userid')),
            ).fetchone()
            if task2user:
                db.execute('UPDATE t2u SET grade = ? WHERE task = ? AND user = ?', (grade, taskid, request.args.get('userid')))
            else:
                db.execute('INSERT INTO t2u (task, user, grade) VALUES (?, ?, ?)', (taskid, request.args.get('userid'), grade))
            db.commit()

        return redirect(url_for('user.usertasks') + '?userid=' + request.args.get('userid'))
    else:
        task_list = db.execute(
            'SELECT t.id, t.name, t2u.grade, t2u.user '
            'FROM user u '
            'LEFT JOIN task t '
            'LEFT JOIN t2u ON t2u.task = t.id AND t2u.user = u.id '
            'WHERE u.id = ? '
            'GROUP BY t.id', (request.args.get('userid'),)
        ).fetchall()
        user = db.execute(
            'SELECT * '
            'FROM user '
            'WHERE id = ?', (request.args.get('userid')),
        ).fetchone()
        return render_template('other/usertasks.html', tasks=task_list, user=user)
