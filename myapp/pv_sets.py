from flask import request, Blueprint
from flask import Flask, jsonify, request, abort
import myapp.business_logic as b_logic

bp = Blueprint('pvsets', __name__, url_prefix='/pv_sets', static_folder='static')


# PROCESS VARIABLE SETS

@bp.route('', methods=['POST'])
def create_new_pv_set():

    b_logic.create_pv_set()

    return "", 201


@bp.route('', methods=['GET'])
def get_pv_sets():
    output = b_logic.get_pv_sets()

    return output

    column_names = ['RUN_ID', 'NAME', 'USER', 'START_DATE', 'END_DATE']

    # Get all records
    data = ProcessVariableSet.query.all()

    if not data:
        abort(400)

    output = []
    for rec in data:
        output_record = {}
        for name in column_names:
            output_record[name] = getattr(rec, name)
        output.append(output_record)

    return jsonify(output)


@bp.route('', methods=['PUT'])
def edit_pv_set(run_id, pv_name):

    return

    # the request should be json and an id must be present
    if not request.json or 'PV_CONTENT' not in request.json:
        abort(400)

    # Get records relating to that pv
    data = ProcessVariables.query.filter_by(RUN_ID=run_id).all()

    if not data:
        abort(400)

    for rec in data:
        if rec.PV_NAME in pv_name:
            rec.PV_CONTENT = request.json.get('PV_CONTENT')
            rec.PV_REASON = request.json.get('PV_REASON')

    db.session.commit()

    return "", 200


@bp.route('/<run_id>', methods=['DELETE'])
def delete_pv_set(run_id=None):
    b_logic.delete_pv_set(run_id)

    return "", 200

    # data = ShiftData.query.filter_by(RUN_ID=run_id).all()
    # for rec in data:
    #     db.session.delete(rec)
    #
    # db.session.commit()
    #
    # return "", 200