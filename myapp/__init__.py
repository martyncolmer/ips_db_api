from flask import Flask, render_template, redirect, url_for
import logging
from logging.handlers import RotatingFileHandler
import inspect

from myapp.models import db
from . import settings


def create_app(test_config=None):

    # Create and configure the app
    app = Flask(__name__)

    app.config.from_object(settings)

    # Configuration needed by SQLAlchemy
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ips_data.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Instead of using db = SQLAlchemy(app)
    db.init_app(app)

    # initialize the log handler
    log_handler = RotatingFileHandler('flask_logger.log', maxBytes=2000, backupCount=2)
    # set the log handler level
    log_handler.setLevel(logging.INFO)

    # set the app logger level
    app.logger.setLevel(logging.INFO)

    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(funcName)s - %(levelname)s - %(message)s')
    log_handler.setFormatter(formatter)

    app.logger.addHandler(log_handler)

    if test_config:
            # Override default Settings with test config if passed in
            app.config.from_mapping(test_config)

    # Register Blueprints
    from . import runs, run_steps, pv_sets, pv, survey_subsample
    app.register_blueprint(runs.bp)
    app.register_blueprint(run_steps.bp)
    app.register_blueprint(pv_sets.bp)
    app.register_blueprint(pv.bp)
    app.register_blueprint(survey_subsample.bp)

    # Register Simple Index Page
    @app.route('/')
    def index():
        return redirect(url_for('runs.get_runs'))

    return app
