from flask import request, Blueprint
from flask import Flask, jsonify, request, abort
import myapp.business_logic as b_logic
import myapp.persistence_layer as p_layer

bp = Blueprint('run_steps', __name__, url_prefix='/run_steps', static_folder='static')


@bp.route('/<run_id>', methods=['GET'])
@bp.route('/<run_id>', methods=['GET'])
def get_run_steps(run_id):
    output = b_logic.get_run_steps(run_id)

    return output


@bp.route('/<run_id>', methods=['POST'])
def create_run_steps(run_id):
    b_logic.create_run_steps(run_id)

    return "", 201


@bp.route('/<run_id>/<value>', methods=['PUT'])
@bp.route('/<run_id>/<value>/<step_number>', methods=['PUT'])
def update_run_steps(run_id, value, step_number=None):
    b_logic.edit_run_steps(run_id, value, step_number)

    return "", 200

    # steps = {1: 'Calculate Shift Weight',
    #          2: 'Calculate Non-Response Weight',
    #          3: 'Calculate Minimums Weight',
    #          4: 'Calculate Traffic Weight',
    #          5: 'Calculate Unsampled Weight',
    #          6: 'Calculate Imbalance Weight',
    #          7: 'Calculate Final Weight',
    #          8: 'Stay Imputation',
    #          9: 'Fares Imputation',
    #          10: 'Spend Imputation',
    #          11: 'Rail Imputation',
    #          12: 'Regional Weight',
    #          13: 'Town Stay and Expenditure Imputation',
    #          14: 'Air Miles',
    #          }
    #
    # if not run_id:
    #     abort(400)
    #
    # if not value:
    #     abort(400)
    #
    # data = RunSteps.query.all()
    #
    # if not data:
    #     abort(400)
    #
    # for x in data:
    #     if x.RUN_ID == run_id:
    #         if step_number:
    #             if x.NUMBER == step_number:
    #                 x.STATUS = value
    #         else:
    #             x.STATUS = value
    #
    # db.session.commit()
    #
    # return "", 200
