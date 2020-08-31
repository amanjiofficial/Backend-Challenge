from flask import Flask, render_template
from .db import db
from .server import bluePrint
import os


def create_app():
    app = Flask(__name__, template_folder="../templates")
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.register_blueprint(bluePrint)

    @app.route('/')
    def index():
        return render_template("index.html")

    return app