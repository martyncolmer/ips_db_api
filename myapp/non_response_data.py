from flask import Blueprint
import myapp.business_logic as b_logic

bp = Blueprint('non_response_data', __name__, url_prefix='/NON_RESPONSE_DATA', static_folder='static')


@bp.route('/<run_id>', methods=['GET'])
def get_non_response_data(run_id):
    output = b_logic.get_data(run_id, 'NON_RESPONSE_DATA')

    return output
