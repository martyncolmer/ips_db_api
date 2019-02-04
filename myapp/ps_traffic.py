from flask import request, Blueprint
from flask import Flask, jsonify, request, abort
import myapp.business_logic as b_logic

bp = Blueprint('ps_traffic', __name__, url_prefix='/PS_TRAFFIC', static_folder='static')


@bp.route('/<run_id>', methods=['GET'])
def get_survey_subsample(run_id):
    output = b_logic.get_data(run_id, 'PS_TRAFFIC')

    return output
