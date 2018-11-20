import os
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_app import db, server

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    Bootstrap(app)
    app.config.from_mapping(
        SECRET_KEY='blah',
        DATABASE=os.path.join(app.instance_path, 'sqlite.db'),
    )

    db.init_app(app)
    app.register_blueprint(server.bp)

    app.add_url_rule('/', endpoint='index')
    return app