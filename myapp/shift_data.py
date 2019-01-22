from flask import request, Blueprint
from flask import Flask, jsonify, request, abort
import myapp.business_logic as b_logic

bp = Blueprint('shift_data', __name__, url_prefix='/SHIFT_DATA', static_folder='static')


@bp.route('/<run_id>', methods=['GET'])
@bp.route('/<run_id>', methods=['GET'])
def get_shift_data(run_id):
    output = b_logic.get_data(run_id, 'SHIFT_DATA')

    return output

# @bp.route('/<run_id>', methods=['POST'])
# def import_shift_data(run_id):
#     b_logic.import_data(run_id, 'SHIFT_DATA')
#
#     return "", 201
