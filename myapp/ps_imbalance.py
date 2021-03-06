from flask import request, Blueprint
from flask import Flask, jsonify, request, abort
import myapp.business_logic as b_logic

bp = Blueprint('ps_imbalance', __name__, url_prefix='/PS_IMBALANCE', static_folder='static')


@bp.route('/<run_id>', methods=['GET'])
def get_survey_subsample(run_id):
    output = b_logic.get_data(run_id, 'PS_IMBALANCE')

    return output
