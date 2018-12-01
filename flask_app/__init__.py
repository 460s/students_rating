import os
import json
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_app import db, server


def get_config(path):
    with open(os.path.join(path, 'app.config'), 'w+') as json_data:
        try:
            config = json.load(json_data)
        except json.decoder.JSONDecodeError:
            config = {}
        if not hasattr(config, 'secret_key') or not config['secret_key']:
            config['secret_key'] = str(os.urandom(16).hex())
        json_data.write(json.dumps(config))
        return config


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    Bootstrap(app)
    config = get_config(app.instance_path)
    app.config.from_mapping(
        SECRET_KEY=config['secret_key'],
        DATABASE=os.path.join(app.instance_path, 'sqlite.db'),
    )
    db.init_app(app)
    app.register_blueprint(server.bp)
    app.add_url_rule('/', endpoint='index')
    return app
