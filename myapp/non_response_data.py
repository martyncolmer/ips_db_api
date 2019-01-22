from flask import request, Blueprint
from flask import Flask, jsonify, request, abort
import myapp.business_logic as b_logic

bp = Blueprint('non_response_data', __name__, url_prefix='/NON_RESPONSE_DATA', static_folder='static')


@bp.route('/<run_id>', methods=['GET'])
def get_non_response_data(run_id):
    output = b_logic.get_data(run_id, 'NON_RESPONSE_DATA')

    return output


# @bp.route('/<run_id>', methods=['POST'])
# def import_non_response_data(run_id):
#     b_logic.import_data(run_id, 'NON_RESPONSE_DATA')
#
#     return "", 201
