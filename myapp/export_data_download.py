from flask import Blueprint
import myapp.business_logic as b_logic

bp = Blueprint('export_data_download', __name__, url_prefix='/EXPORT_DATA_DOWNLOAD', static_folder='static')


@bp.route('', methods=['POST'])
def create_export_data_download():
    # function_name = {"Survey Subsample": None,
    #                  "Final Weight Summary": None,
    #                  "Shift": get_shift_data,
    #                  "Non-Response": get_non_response_data,
    #                  "Shift Weight Summary": None,
    #                  "Non Response Weight Summary": None,
    #                  "Minimum Weight Summary": None,
    #                  "Traffic Weight Summary": get_traffic_data,
    #                  "Unsampled Traffic Weight Summary": get_unsampled_data,
    #                  "Imbalance Weight Summary": get_imbalance_weight}

    # the request should be json
    b_logic.create_export_data_download()

    return "", 201


@bp.route('/<run_id>', methods=['GET'])
@bp.route('/<run_id>/<file_name>/<source_table>', methods=['GET'])
def get_export_data_download(run_id, file_name=None, source_table=None):
    output = b_logic.get_export_data_download(run_id, file_name, source_table)

    return output
