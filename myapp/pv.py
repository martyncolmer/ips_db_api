from flask import request, Blueprint
from flask import Flask, jsonify, request, abort
import myapp.business_logic as b_logic

bp = Blueprint('process_variables', __name__, url_prefix='/process_variables', static_folder='static')


# PROCESS VARIABLES

@bp.route('/<run_id>', methods=['POST'])
def create_process_variables(run_id):
    b_logic.create_process_variables(run_id)

    return "", 201


@bp.route('/', methods=['GET'])
@bp.route('/<run_id>', methods=['GET'])
def get_process_variables(run_id=None):
    output = b_logic.get_process_variables(run_id)

    return output


@bp.route('/<run_id>', methods=['DELETE'])
def delete_process_variables(run_id=None):
    b_logic.delete_process_variables(run_id)

    return "", 200

