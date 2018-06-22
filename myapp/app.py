import json
from flask import Flask, jsonify, request, abort, redirect

from myapp.models import db, Run, RunSteps, ProcessVariableSet, ProcessVariables, \
    ShiftData, NonResponseData, TrafficData, UnsampledOOHData, \
    ImbalanceWeight, ExportDataDownload

app = Flask(__name__)

# Configuration needed by SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ips_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Instead of using db = SQLAlchemy(app)
db.init_app(app)

# RUNS

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


# RUN STEPS

@app.route('/run_steps/<run_id>', methods=['POST'])
def create_run_steps(run_id=None):
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


@app.route('/run_steps', methods=['GET'])
@app.route('/RUN_STEPS', methods=['GET'])
@app.route('/run_steps/<run_id>', methods=['GET'])
@app.route('/RUN_STEPS/<run_id>', methods=['GET'])
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


@app.route('/run_steps/<run_id>/<value>', methods=['PUT'])
@app.route('/run_steps/<run_id>/<value>/<step_number>', methods=['PUT'])
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


# PROCESS VARIABLE SETS

@app.route('/pv_sets', methods=['POST'])
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


@app.route('/pv_sets', methods=['GET'])
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


@app.route('/pv_sets', methods=['PUT'])
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


# SHIFT DATA

@app.route('/SHIFT_DATA/<run_id>', methods=['POST'])
@app.route('/shift_data/<run_id>', methods=['POST'])
def import_shift_data(run_id):

    if not request.json:
        abort(400)

    data = request.json

    for rec in data:
        run = ShiftData(RUN_ID=rec['RUN_ID'],
                        YEAR=rec['YEAR'],
                        MONTH=rec['MONTH'],
                        DATA_SOURCE_ID=rec['DATA_SOURCE_ID'],
                        PORTROUTE=rec['PORTROUTE'],
                        WEEKDAY=rec['WEEKDAY'],
                        ARRIVEDEPART=rec['ARRIVEDEPART'],
                        TOTAL=rec['TOTAL'],
                        AM_PM_NIGHT=rec['AM_PM_NIGHT'])
        db.session.add(run)
    db.session.commit()

    return "", 200


@app.route('/SHIFT_DATA', methods=['GET'])
@app.route('/shift_data', methods=['GET'])
@app.route('/SHIFT_DATA/<run_id>', methods=['GET'])
@app.route('/shift_data/<run_id>', methods=['GET'])
@app.route('/SHIFT_DATA/<run_id>/<data_source>', methods=['GET'])
@app.route('/shift_data/<run_id>/<data_source>', methods=['GET'])
def get_shift_data(run_id=None, data_source='0'):
    column_names = ['RUN_ID', 'YEAR', 'MONTH', 'DATA_SOURCE_ID', 'PORTROUTE', 'WEEKDAY', 'ARRIVEDEPART', 'TOTAL',
                    'AM_PM_NIGHT']

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


# NON RESPONSE DATA

@app.route('/NON_RESPONSE_DATA/<run_id>', methods=['POST'])
@app.route('/non_response_data/<run_id>', methods=['POST'])
def import_non_response_data(run_id):

    if not request.json:
        abort(400)

    data = request.json

    for rec in data:
        run = NonResponseData(RUN_ID=rec['RUN_ID'],
                              YEAR=rec['YEAR'],
                              MONTH=rec['MONTH'],
                              DATA_SOURCE_ID=rec['DATA_SOURCE_ID'],
                              PORTROUTE=rec['PORTROUTE'],
                              WEEKDAY=rec['WEEKDAY'],
                              ARRIVEDEPART=rec['ARRIVEDEPART'],
                              AM_PM_NIGHT=rec['AM_PM_NIGHT'],
                              SAMPINTERVAL=rec['SAMPINTERVAL'],
                              MIGTOTAL=rec['MIGTOTAL'],
                              ORDTOTAL=rec['ORDTOTAL'])
        db.session.add(run)
    db.session.commit()

    return "", 200


@app.route('/NON_RESPONSE_DATA', methods=['GET'])
@app.route('/non_response_data', methods=['GET'])
@app.route('/NON_RESPONSE_DATA/<run_id>', methods=['GET'])
@app.route('/non_response_data/<run_id>', methods=['GET'])
@app.route('/NON_RESPONSE_DATA/<run_id>/<data_source>', methods=['GET'])
@app.route('/non_response_data/<run_id>/<data_source>', methods=['GET'])
def get_non_response_data(run_id=None, data_source='0'):
    column_names = ['RUN_ID', 'YEAR', 'MONTH', 'DATA_SOURCE_ID', 'PORTROUTE', 'WEEKDAY', 'ARRIVEDEPART', 'AM_PM_NIGHT',
                    'SAMPINTERVAL', 'MIGTOTAL', 'ORDTOTAL']

    data = NonResponseData.query.all()

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


# TRAFFIC DATA

@app.route('/TRAFFIC_DATA/<run_id>', methods=['POST'])
@app.route('/traffic_data/<run_id>', methods=['POST'])
def import_traffic_data(run_id):

    if not request.json:
        abort(400)

    data = request.json

    for rec in data:
        run = TrafficData(RUN_ID=rec['RUN_ID'],
                          YEAR=rec['YEAR'],
                          MONTH=rec['MONTH'],
                          DATA_SOURCE_ID=rec['DATA_SOURCE_ID'],
                          PORTROUTE=rec['PORTROUTE'],
                          ARRIVEDEPART=rec['ARRIVEDEPART'],
                          TRAFFICTOTAL=rec['TRAFFICTOTAL'],
                          PERIODSTART=rec['PERIODSTART'],
                          PERIODEND=rec['PERIODEND'],
                          AM_PM_NIGHT=rec['AM_PM_NIGHT'],
                          HAUL=rec['HAUL'],
                          VEHICLE=rec['VEHICLE'])
        db.session.add(run)
    db.session.commit()

    return "", 200


@app.route('/TRAFFIC_DATA', methods=['GET'])
@app.route('/traffic_data', methods=['GET'])
@app.route('/TRAFFIC_DATA/<run_id>', methods=['GET'])
@app.route('/traffic_data/<run_id>', methods=['GET'])
@app.route('/TRAFFIC_DATA/<run_id>/<data_source>', methods=['GET'])
@app.route('/traffic_data/<run_id>/<data_source>', methods=['GET'])
def get_traffic_data(run_id=None, data_source='0'):
    column_names = ['RUN_ID', 'YEAR', 'MONTH', 'DATA_SOURCE_ID', 'PORTROUTE', 'ARRIVEDEPART', 'TRAFFICTOTAL',
                    'PERIODSTART', 'PERIODEND', 'AM_PM_NIGHT', 'HAUL', 'VEHICLE']

    data = TrafficData.query.all()

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


# UNSAMPLED OOH DATA

@app.route('/UNSAMPLED_OOH_DATA/<run_id>', methods=['POST'])
@app.route('/unsampled_ooh_data/<run_id>', methods=['POST'])
def import_unsampled_data(run_id):

    if not request.json:
        abort(400)

    data = request.json

    for rec in data:
        run = UnsampledOOHData(RUN_ID=rec['RUN_ID'],
                               YEAR=rec['YEAR'],
                               MONTH=rec['MONTH'],
                               DATA_SOURCE_ID=rec['DATA_SOURCE_ID'],
                               PORTROUTE=rec['PORTROUTE'],
                               REGION=rec['REGION'],
                               ARRIVEDEPART=rec['ARRIVEDEPART'],
                               UNSAMP_TOTAL=rec['UNSAMP_TOTAL'])
        db.session.add(run)
    db.session.commit()

    return "", 200


@app.route('/UNSAMPLED_OOH_DATA', methods=['GET'])
@app.route('/unsampled_ooh_data', methods=['GET'])
@app.route('/UNSAMPLED_OOH_DATA/<run_id>', methods=['GET'])
@app.route('/unsampled_ooh_data/<run_id>', methods=['GET'])
@app.route('/UNSAMPLED_OOH_DATA/<run_id>/<data_source>', methods=['GET'])
@app.route('/unsampled_ooh_data/<run_id>/<data_source>', methods=['GET'])
def get_unsampled_data(run_id=None, data_source='0'):
    column_names = ['RUN_ID', 'YEAR', 'MONTH', 'DATA_SOURCE_ID', 'PORTROUTE', 'REGION', 'ARRIVEDEPART', 'UNSAMP_TOTAL']

    data = UnsampledOOHData.query.all()

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


# IMBALANCE WEIGHT

@app.route('/IMBALANCE_WEIGHT', methods=['GET'])
@app.route('/imbalance_weight', methods=['GET'])
@app.route('/IMBALANCE_WEIGHT/<run_id>', methods=['GET'])
@app.route('/imbalance_weight/<run_id>', methods=['GET'])
def get_imbalance_weight(run_id=None):
    column_names = ['RUN_ID', 'FLOW', 'SUM_PRIOR_WT', 'SUM_IMBAL_WT']

    data = ImbalanceWeight.query.all()

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


# EXPORT DATA

# @app.route('/EXPORT_DATA_DOWNLOAD/<run_id>/<filename>/<source_table>/<date_created>', methods=['POST'])
# @app.route('/export_data_download/<run_id>/<filename>/<source_table>/<date_created>', methods=['POST'])
@app.route('/EXPORT_DATA_DOWNLOAD', methods=['POST'])
@app.route('/export_data_download', methods=['POST'])
@app.route('/EXPORT_DATA_DOWNLOAD/<run_id>', methods=['POST'])
@app.route('/export_data_download/<run_id>', methods=['POST'])
def create_export_data_download(run_id=None):
    print("create_export_data_download")
    # the request should be json and an FILENAME must be present
    print(request.json)
    if not request.json:
        abort(400)
    json_data = request.json

    # HARD-CODED for scope.  Need list of source_table names to correspond with routes
    # table = app.get('http://ips-db.apps.cf1.ons.statistics.gov.uk/' + source_table + '/' + run_id)
    if not run_id:
        response = get_imbalance_weight()
        table = response.json
    else:
        table = app.get('http://ips-db.apps.cf1.ons.statistics.gov.uk/IMBALANCE_WEIGHT/' + run_id)

    # Convert json import to string
    data = json.dumps(table)

    new_rec = ExportDataDownload(RUN_ID=json_data['RUN_ID'],
                                 DOWNLOADABLE_DATA=data,
                                 FILENAME=json_data['FILENAME'],
                                 SOURCE_TABLE=json_data['SOURCE_TABLE'],
                                 DATE_CREATED=json_data['DATE_CREATED'])
    print(new_rec)

    db.session.add(new_rec)
    db.session.commit()

    return "", 201


# @app.route('/EXPORT_DATA_DOWNLOAD', methods=['GET'])
# @app.route('/export_data_download', methods=['GET'])
@app.route('/EXPORT_DATA_DOWNLOAD/<run_id>', methods=['GET'])
@app.route('/export_data_download/<run_id>', methods=['GET'])
@app.route('/EXPORT_DATA_DOWNLOAD', methods=['GET'])
@app.route('/export_data_download', methods=['GET'])
def get_export_data_download(run_id=None):
    column_names = ['RUN_ID', 'DOWNLOADABLE_DATA', 'FILENAME', 'SOURCE_TABLE', 'DATE_CREATED']

    data = ExportDataDownload.query.all()

    if not data:
        abort(400)

    output = []
    for rec in data:
        output_record = {}
        for name in column_names:
            output_record[name] = getattr(rec, name)
        output.append(output_record)

    # Filter by run_id if provided
    if run_id:
        run_filtered = []

        for rec in output:
            if rec['RUN_ID'] == run_id:
                run_filtered.append(rec)

        if len(run_filtered) == 0:
            abort(400)

        output = run_filtered

    return jsonify(output)


@app.route('/test_json', methods=['GET'])
def get_json():
    output = []
    json_data = {'RUN_ID': 'Automated-Run_ID', 'YEAR': 'YEAR', 'MONTH': 'MONTH',
                 'DATA_SOURCE_ID': 'DATA_SOURCE_ID', 'PORTROUTE': 'PORTROUTE', 'WEEKDAY': 'WEEKDAY',
                 'ARRIVEDEPART': 'ARRIVEDEPART', 'TOTAL': 'TOTAL', 'AM_PM_NIGHT': 'AM_PM_NIGHT'}
    json_data2 = {'RUN_ID': 'Automated-Run_ID', 'YEAR': 'YEAR-2', 'MONTH': 'MONTH-2',
                 'DATA_SOURCE_ID': 'DATA_SOURCE_ID-2', 'PORTROUTE': 'PORTROUTE-2', 'WEEKDAY': 'WEEKDAY-2',
                 'ARRIVEDEPART': 'ARRIVEDEPART-2', 'TOTAL': 'TOTAL-2', 'AM_PM_NIGHT': 'AM_PM_NIGHT-2'}

    output.append(json_data)
    output.append(json_data2)

    return jsonify(output)


