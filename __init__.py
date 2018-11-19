import os
from flask import Flask
from flask_simplelogin import SimpleLogin
import db, server

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='blah',
        DATABASE=os.path.join('db/sqlite.db'),
    )


    db.init_app(app)
    app.register_blueprint(server.bp)

    #app.add_url_rule('/', endpoint='index')
    return app