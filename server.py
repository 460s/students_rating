from flask import Flask
from flask_simplelogin import SimpleLogin
from flask import render_template
from flask import request
from flask import send_from_directory
import sqlite3
app = Flask(__name__)
SimpleLogin(app)

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/reg', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        return "ds"
    else:
        return send_from_directory(app.static_folder, "templates/registration.html")
    # conn = sqlite3.connect("db/sqlite.db")
    # cursor = conn.cursor()
    # cursor.execute("""INSERT INTO users VALUES (NULL, 'test3', 'pass', 'http://hghghg')""")
    # conn.commit()
    return "ok"

# def main():


# if __name__ == "__main__":
#     main()

# def init_db():
#     db = get_db()
#     with app.open_resource('schema.sql', mode='r') as f:
#         db.cursor().executescript(f.read())
#     db.commit()
#
# @app.cli.command('initdb')
# def initdb_command():
#     """Initializes the database."""
#     init_db()
#     print('Initialized the database.')