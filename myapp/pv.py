from flask import request, Blueprint
from flask import Flask, jsonify, request, abort
from myapp.models import db, Run

bp = Blueprint('process_variables', __name__, url_prefix='/process_variables', static_folder='static')


# PROCESS VARIABLES

@app.route('/process_variables/<run_id>/<template_id>', methods=['POST'])
def create_process_variables(run_id, template_id):

    # Get the process variables records associated with the template id
    data = ProcessVariables.query.filter_by(RUN_ID=template_id).all()

    # Quit if no date is returned (the template id has no associated process variables)
    if not data:
        abort(400)

    # Loop through and copy the template into the new pv set using the run id specified.
    for rec in data:
        new_pv = ProcessVariables(RUN_ID=run_id,
                                  PV_NAME=rec.PV_NAME,
                                  PV_CONTENT=rec.PV_CONTENT,
                                  PV_REASON=rec.PV_REASON)
        db.session.add(new_pv)

    db.session.commit()

    return "", 201


@app.route('/process_variables', methods=['GET'])
@app.route('/process_variables/<run_id>', methods=['GET'])
def get_process_variables(run_id=None):
    column_names = ['RUN_ID', 'PV_NAME', 'PV_CONTENT', 'PV_REASON']
    # if a run id is provided search for this specific run
    if run_id:
        # Get records relating to that pv
        data = ProcessVariables.query.filter_by(RUN_ID=run_id).all()
    else:
        # Get all records
        data = ProcessVariables.query.all()

    if not data:
        abort(400)

    output = []
    for rec in data:
        output_record = {}
        for name in column_names:
            output_record[name] = getattr(rec, name)
        output.append(output_record)

    return jsonify(output)


@app.route('/process_variables', methods=['PUT'])
def update_process_variable():

    # the request should be json and an id must be present
    if not request.json:
        abort(400)

    updated_data = request.json

    # Get records relating to that pv
    data = ProcessVariables.query.filter_by(RUN_ID=updated_data['RUN_ID']).all()

    if not data:
        abort(400)

    for rec in data:
        if rec.PV_NAME in updated_data['PV_NAME']:
            rec.PV_CONTENT = updated_data['PV_CONTENT']
            rec.PV_REASON = updated_data['PV_REASON']

    db.session.commit()

    return "", 200
