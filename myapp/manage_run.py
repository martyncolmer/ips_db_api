from flask import Blueprint
import myapp.business_logic as b_logic

bp = Blueprint('manage_run', __name__, url_prefix='/manage_run', static_folder='static')


@bp.route('/start_run/<run_id>', methods=['POST'])
def start_run(run_id):
    b_logic.start_run(run_id)

    return '', 200
