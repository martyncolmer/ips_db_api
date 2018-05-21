from flask import Flask, jsonify, request, abort

from myapp.models import db, Run, ShiftData, RunStatus

app = Flask(__name__)

# Configuration needed by SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ips_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Instead of using db = SQLAlchemy(app)
db.init_app(app)


@app.route('/runs', methods=['GET'])
@app.route('/runs/<run_id>', methods=['GET'])
def get_runs(run_id=None):

    column_names = ['id', 'name', 'desc', 'start_date', 'end_date', 'status', 'type']
    # if a run id is provided search for this specific run
    if run_id:
        # Get a single record
        data = Run.query.get(run_id)
        if not data:
            abort(400)
        output = {}
        for name in column_names:
            output[name] = getattr(data, name)
    else:
        # Get all records
        data = Run.query.all()

        output = []
        for rec in data:
            output_record = {}
            for name in column_names:
                output_record[name] = getattr(rec, name)
            output.append(output_record)

    return jsonify(output)


@app.route('/runs', methods=['POST'])
def create_run():
    # the request should be json and an id must be present
    if not request.json or 'id' not in request.json:
        abort(400)

    run = Run(id=request.json['id'],
              name=request.json['name'],
              desc=request.json.get('desc', ""),
              start_date=request.json.get('start_date', ""),
              end_date=request.json.get('end_date', ""),
              status=request.json.get('status', ""),
              type=request.json.get('type', ""))
    db.session.add(run)
    db.session.commit()

    return "", 201


@app.route('/runs/<run_id>', methods=['PUT'])
def update_run(run_id):
    # the request should be json and an id must be present
    if not request.json or not run_id:
        abort(400)

    data = Run.query.get(run_id)

    if not data:
        abort(400)

    data.name = request.json['name']
    data.desc = request.json.get('desc', "")
    data.start_date = request.json.get('start_date', "")
    data.end_date = request.json.get('end_date', "")
    data.status = request.json.get('status', "")
    data.type = request.json.get('type', "")

    db.session.commit()

    return "", 200


@app.route('/SHIFT_DATA', methods=['GET'])
@app.route('/shift_data', methods=['GET'])
@app.route('/SHIFT_DATA/<run_id>', methods=['GET'])
@app.route('/shift_data/<run_id>', methods=['GET'])
@app.route('/SHIFT_DATA/<run_id>/<data_source>', methods=['GET'])
@app.route('/shift_data/<run_id>/<data_source>', methods=['GET'])
def get_shift_data(run_id=None, data_source='0'):

    column_names = ['RUN_ID', 'YEAR', 'MONTH', 'DATA_SOURCE_ID', 'PORTROUTE', 'WEEKDAY', 'ARRIVEDEPART', 'TOTAL', 'AM_PM_NIGHT']

    data = ShiftData.query.all()

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

    if data_source != '0':
        ds_filtered = []

        for rec in output:
            if rec['DATA_SOURCE_ID'] == data_source:
                ds_filtered.append(rec)

        if len(ds_filtered) == 0:
            abort(400)

        output = ds_filtered

    return jsonify(output)


@app.route('/run_status', methods=['GET'])
@app.route('/RUN_STATUS', methods=['GET'])
@app.route('/run_status/<run_id>', methods=['GET'])
@app.route('/RUN_STATUS/<run_id>', methods=['GET'])
def get_run_status(run_id=None):

    column_names = ['RUN_ID', 'STEP', 'STATUS']

    data = RunStatus.query.all()

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
