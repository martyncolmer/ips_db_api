from flask import request, Blueprint
from flask import Flask, jsonify, request, abort
import myapp.business_logic as b_logic

bp = Blueprint('traffic_data', __name__, url_prefix='/TRAFFIC_DATA', static_folder='static')


@bp.route('/<run_id>/<data_source>', methods=['GET'])
def get_traffic_data(run_id, data_source):
    output = b_logic.get_data(run_id, 'TRAFFIC_DATA', datasource=data_source)

    return output


# @bp.route('/<run_id>', methods=['POST'])
# def import_traffic_data(run_id):
#     b_logic.import_data(run_id, 'TRAFFIC_DATA')
#
#     return "", 201
