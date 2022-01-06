from flask import Flask

from extensions import db
from routes import net


def create_app(config='settings.py'):
    app = Flask(__name__)

    app.config.from_pyfile(config)

    app.register_blueprint(net)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app
