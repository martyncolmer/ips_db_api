from flask import Flask, render_template, redirect, url_for
import logging
from logging.handlers import RotatingFileHandler
import inspect

from . import settings


def create_app(test_config=None):

    # Create and configure the app
    app = Flask(__name__)

    app.config.from_object(settings)

    # Configuration needed by SQLAlchemy
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ips_data.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Instead of using db = SQLAlchemy(app)
    #db.init_app(app)

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
    from . import runs, run_steps, pv_sets, pv, export_data_download, response, manage_run, \
        survey_subsample, shift_data, non_response_data, traffic_data, unsampled_data, \
        ps_final, ps_imbalance, ps_minimums, ps_non_response, ps_shift_data, ps_traffic, ps_unsampled_ooh

    # Run tables
    app.register_blueprint(runs.bp)
    app.register_blueprint(run_steps.bp)
    app.register_blueprint(pv.bp)
    app.register_blueprint(pv_sets.bp)
    app.register_blueprint(response.bp)
    app.register_blueprint(manage_run.bp)
    app.register_blueprint(export_data_download.bp)

    # Data tables
    app.register_blueprint(survey_subsample.bp)
    app.register_blueprint(shift_data.bp)
    app.register_blueprint(non_response_data.bp)
    app.register_blueprint(traffic_data.bp)
    app.register_blueprint(unsampled_data.bp)

    # Summary tables
    app.register_blueprint(ps_shift_data.bp)
    app.register_blueprint(ps_non_response.bp)
    app.register_blueprint(ps_minimums.bp)
    app.register_blueprint(ps_traffic.bp)
    app.register_blueprint(ps_unsampled_ooh.bp)
    app.register_blueprint(ps_imbalance.bp)
    app.register_blueprint(ps_final.bp)

    # Register Simple Index Page
    @app.route('/')
    def index():
        return redirect(url_for('runs.get_runs'))

    return app
