from flask import Blueprint
import myapp.business_logic as b_logic

bp = Blueprint('runs', __name__, url_prefix='/runs', static_folder='static')


@bp.route('', methods=['GET'])
@bp.route('/<run_id>', methods=['GET'])
def get_runs(run_id=None):
    output = b_logic.get_run()

    return output


@bp.route('', methods=['POST'])
def create_run():
    b_logic.create_run()

    return "", 201


@bp.route('/<run_id>', methods=['PUT'])
def edit_run(run_id):
    b_logic.edit_run(run_id)

    return "", 200
