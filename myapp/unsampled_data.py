from flask import Blueprint
import myapp.business_logic as b_logic

bp = Blueprint('unsampled_ooh_data', __name__, url_prefix='/UNSAMPLED_OOH_DATA', static_folder='static')


@bp.route('/<run_id>', methods=['GET'])
def get_unsampled_ooh_data(run_id):
    output = b_logic.get_data(run_id, 'UNSAMPLED_OOH_DATA')

    return output
