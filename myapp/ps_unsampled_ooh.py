from flask import request, Blueprint
from flask import Flask, jsonify, request, abort
import myapp.business_logic as b_logic

bp = Blueprint('ps_unsampled_ooh', __name__, url_prefix='/PS_UNSAMPLED_OOH', static_folder='static')


@bp.route('/<run_id>', methods=['GET'])
def get_survey_subsample(run_id):
    output = b_logic.get_data(run_id, 'PS_UNSAMPLED_OOH')

    return output
