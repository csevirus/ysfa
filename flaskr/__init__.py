import os
from flask import (
    Flask, redirect, render_template, url_for
)

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='iq\x9f\xa4\x0e,\xf4\x88z#\xc0\x0c\x12\x12\x0ex',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
        INSTANCE_PATH = app.instance_path
    )
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    from . import db
    db.init_app(app)
    from . import auth
    app.register_blueprint(auth.bp)
    from . import myfiles
    app.register_blueprint(myfiles.bp)
    @app.route('/')
    def index():
        return render_template("index.html")
    return app
