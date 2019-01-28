from flask import Blueprint
import myapp.business_logic as b_logic

bp = Blueprint('traffic_data', __name__, url_prefix='/TRAFFIC_DATA', static_folder='static')


@bp.route('/<run_id>/<data_source>', methods=['GET'])
def get_traffic_data(run_id, data_source):
    output = b_logic.get_data(run_id, 'TRAFFIC_DATA', datasource=data_source)

    return output
