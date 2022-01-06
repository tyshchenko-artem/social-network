from flask import Flask

from app.extensions import db
from app.routes import net


def create_app(config='settings.py'):
    app = Flask(__name__)

    app.config.from_pyfile(config)

    db.init_app(app)

    app.register_blueprint(net)

    return app
