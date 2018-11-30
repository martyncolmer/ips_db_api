from flask import request, Blueprint
from flask import Flask, jsonify, request, abort
from myapp.models import db, RunSteps
import myapp.business_logic as b_logic
import myapp.persistence_layer as p_layer

bp = Blueprint('response', __name__, url_prefix='/RESPONSE', static_folder='static')


@bp.route('/<run_id>', methods=['GET'])
@bp.route('/<run_id>', methods=['GET'])
def get_run_steps(run_id):
    output = b_logic.get_response(run_id)

    return output


@bp.route('/<run_id>/<step_number>', methods=['POST'])
def create_run_steps(run_id, step_number):
    b_logic.create_response(run_id, step_number)

    return "", 201
