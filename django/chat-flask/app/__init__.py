import os
from flask import Flask

def create_app(config_class='config.Config'):
    app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), '../templates'))
    app.config.from_object(config_class)

    from .routes import main
    app.register_blueprint(main)

    return app
