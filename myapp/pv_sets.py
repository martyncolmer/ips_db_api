from flask import request, Blueprint
from flask import Flask, jsonify, request, abort
from myapp.models import db, ProcessVariableSet

bp = Blueprint('pvsets', __name__, url_prefix='/pvsets', static_folder='static')


# PROCESS VARIABLE SETS

@bp.route('/we', methods=['POST'])
def create_new_pv_set():
    # the request should be json and an id must be present
    if not request.json or 'RUN_ID' not in request.json:
        abort(400)

    pv_set = ProcessVariableSet(RUN_ID=request.json['RUN_ID'],
                                NAME=request.json['NAME'],
                                USER=request.json['USER'],
                                START_DATE=request.json['START_DATE'],
                                END_DATE=request.json['END_DATE'])
    db.session.add(pv_set)
    db.session.commit()

    return "", 201


@bp.route('/we', methods=['GET'])
def get_pv_sets():
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


@bp.route('/we', methods=['PUT'])
def update_pv_set(run_id, pv_name):

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
