from flask import request, Blueprint
from flask import Flask, jsonify, request, abort
from myapp.models import db, Run
import myapp.business_logic as b_logic

bp = Blueprint('survey_subsample', __name__, url_prefix='/SURVEY_SUBSAMPLE', static_folder='static')


@bp.route('/<run_id>', methods=['POST'])
def import_shift_data(run_id):
    b_logic.import_data(run_id, 'SHIFT_DATA')

    return "", 201
