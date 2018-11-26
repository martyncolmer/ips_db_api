from flask import request, Blueprint
from flask import Flask, jsonify, request, abort
from myapp.models import db, RunSteps

bp = Blueprint('run_steps', __name__, url_prefix='/run_steps', static_folder='static')


# RUN STEPS

@bp.route('/<run_id>', methods=['POST'])
def create_run_steps(run_id=None):
    return "Dodge", 200

    steps = {1: 'Calculate Shift Weight',
             2: 'Calculate Non-Response Weight',
             3: 'Calculate Minimums Weight',
             4: 'Calculate Traffic Weight',
             5: 'Calculate Unsampled Weight',
             6: 'Calculate Imbalance Weight',
             7: 'Calculate Final Weight',
             8: 'Stay Imputation',
             9: 'Fares Imputation',
             10: 'Spend Imputation',
             11: 'Rail Imputation',
             12: 'Regional Weight',
             13: 'Town Stay and Expenditure Imputation',
             14: 'Air Miles',
             }

    if not run_id:
        abort(400)

    for key, value in steps.items():

        run_status = RunSteps(RUN_ID=run_id,
                              NUMBER=str(key),
                              NAME=value,
                              STATUS='0')
        db.session.add(run_status)
        db.session.commit()

    return "", 201


@bp.route('', methods=['GET'])
@bp.route('', methods=['GET'])
@bp.route('/<run_id>', methods=['GET'])
@bp.route('/<run_id>', methods=['GET'])
def get_run_steps(run_id=None):
    column_names = ['RUN_ID', 'NUMBER', 'NAME', 'STATUS']

    data = RunSteps.query.all()

    if not data:
        abort(400)

    output = []
    for rec in data:
        output_record = {}
        for name in column_names:
            output_record[name] = getattr(rec, name)
        output.append(output_record)

    if run_id:
        run_filtered = []

        for rec in output:
            if rec['RUN_ID'] == run_id:
                run_filtered.append(rec)

        if len(run_filtered) == 0:
            abort(400)

        output = run_filtered

    return jsonify(output)


@bp.route('/<run_id>/<value>', methods=['PUT'])
@bp.route('/<run_id>/<value>/<step_number>', methods=['PUT'])
def update_run_steps(run_id, value, step_number=None):
    steps = {1: 'Calculate Shift Weight',
             2: 'Calculate Non-Response Weight',
             3: 'Calculate Minimums Weight',
             4: 'Calculate Traffic Weight',
             5: 'Calculate Unsampled Weight',
             6: 'Calculate Imbalance Weight',
             7: 'Calculate Final Weight',
             8: 'Stay Imputation',
             9: 'Fares Imputation',
             10: 'Spend Imputation',
             11: 'Rail Imputation',
             12: 'Regional Weight',
             13: 'Town Stay and Expenditure Imputation',
             14: 'Air Miles',
             }

    if not run_id:
        abort(400)

    if not value:
        abort(400)

    data = RunSteps.query.all()

    if not data:
        abort(400)

    for x in data:
        if x.RUN_ID == run_id:
            if step_number:
                if x.NUMBER == step_number:
                    x.STATUS = value
            else:
                x.STATUS = value

    db.session.commit()

    return "", 200
