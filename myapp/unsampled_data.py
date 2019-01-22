from flask import request, Blueprint
from flask import Flask, jsonify, request, abort
import myapp.business_logic as b_logic

bp = Blueprint('unsampled_ooh_data', __name__, url_prefix='/UNSAMPLED_OOH_DATA', static_folder='static')


@bp.route('/<run_id>', methods=['GET'])
def get_unsampled_ooh_data(run_id):
    output = b_logic.get_data(run_id, 'UNSAMPLED_OOH_DATA')

    return output


# @bp.route('/<run_id>', methods=['POST'])
# def import_unsampled_ooh_data(run_id):
#     b_logic.import_data(run_id, 'UNSAMPLED_OOH_DATA')
#
#     return "", 201
