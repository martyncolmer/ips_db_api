import json
from flask import Flask, jsonify, request, abort, redirect

from myapp.models import db, Run, RunSteps, ProcessVariableSet, ProcessVariables, \
    ShiftData, NonResponseData, TrafficData, UnsampledOOHData, \
    ImbalanceWeight, ExportDataDownload, SurveySubsample

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

@app.route('/process_variables/<run_id>', methods=['POST'])
def create_process_variables(run_id):

    if not request.json:
        abort(400)

    data = request.json

    for rec in data:
        new_pv = ProcessVariables(RUN_ID=run_id,
                                  PV_NAME=rec['PV_NAME'],
                                  PV_CONTENT=rec['PV_CONTENT'],
                                  PV_REASON=rec['PV_REASON'])
        db.session.add(new_pv)
    db.session.commit()

    return "", 201

# Old method copying from tamplate

# @app.route('/process_variables/<run_id>/<template_id>', methods=['POST'])
# def create_process_variables(run_id, template_id):
#
#     # Get the process variables records associated with the template id
#     data = ProcessVariables.query.filter_by(RUN_ID=template_id).all()
#
#     # Quit if no date is returned (the template id has no associated process variables)
#     if not data:
#         abort(400)
#
#     # Loop through and copy the template into the new pv set using the run id specified.
#     for rec in data:
#         new_pv = ProcessVariables(RUN_ID=run_id,
#                                   PV_NAME=rec.PV_NAME,
#                                   PV_CONTENT=rec.PV_CONTENT,
#                                   PV_REASON=rec.PV_REASON)
#         db.session.add(new_pv)
#
#     db.session.commit()
#
#     return "", 201


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
        run = ShiftData(RUN_ID=run_id,
                        YEAR=rec['YEAR'],
                        MONTH=rec['MONTH'],
                        DATASOURCE=rec['DATASOURCE'],
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
    column_names = ['RUN_ID', 'YEAR', 'MONTH', 'DATASOURCE', 'PORTROUTE', 'WEEKDAY', 'ARRIVEDEPART', 'TOTAL',
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
            if rec['DATASOURCE'] == data_source:
                ds_filtered.append(rec)

        if len(ds_filtered) == 0:
            abort(400)

        output = ds_filtered

    return jsonify(output)


@app.route('/SHIFT_DATA/<run_id>', methods=['DELETE'])
@app.route('/shift_data/<run_id>', methods=['DELETE'])
def delete_shift_data(run_id=None):
    data = ShiftData.query.filter_by(RUN_ID=run_id).all()
    for rec in data:
        db.session.delete(rec)

    db.session.commit()

    return "", 200

# NON RESPONSE DATA


@app.route('/NON_RESPONSE_DATA/<run_id>', methods=['POST'])
@app.route('/non_response_data/<run_id>', methods=['POST'])
def import_non_response_data(run_id):

    if not request.json:
        abort(400)

    data = request.json

    for rec in data:
        run = NonResponseData(RUN_ID=run_id,
                              YEAR=rec['YEAR'],
                              MONTH=rec['MONTH'],
                              DATASOURCE=rec['DATASOURCE'],
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
    column_names = ['RUN_ID', 'YEAR', 'MONTH', 'DATASOURCE', 'PORTROUTE', 'WEEKDAY', 'ARRIVEDEPART', 'AM_PM_NIGHT',
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
            if rec['DATASOURCE'] == data_source:
                ds_filtered.append(rec)

        if len(ds_filtered) == 0:
            abort(400)

        output = ds_filtered

    return jsonify(output)


@app.route('/NON_RESPONSE_DATA/<run_id>', methods=['DELETE'])
@app.route('/non_response_data/<run_id>', methods=['DELETE'])
def delete_non_response_data(run_id=None):
    data = NonResponseData.query.filter_by(RUN_ID=run_id).all()
    for rec in data:
        db.session.delete(rec)

    db.session.commit()

    return "", 200

# TRAFFIC DATA

@app.route('/TRAFFIC_DATA/<run_id>', methods=['POST'])
@app.route('/traffic_data/<run_id>', methods=['POST'])
def import_traffic_data(run_id):

    if not request.json:
        abort(400)

    data = request.json

    for rec in data:
        run = TrafficData(RUN_ID=run_id,
                          YEAR=rec['YEAR'],
                          MONTH=rec['MONTH'],
                          DATASOURCE=rec['DATASOURCE'],
                          PORTROUTE=rec['PORTROUTE'],
                          ARRIVEDEPART=rec['ARRIVEDEPART'],
                          TRAFFICTOTAL=rec['TRAFFICTOTAL'],
                          PERIODSTART=rec['PERIODSTART'],
                          PERIODEND=rec['PERIODEND'],
                          AM_PM_NIGHT=rec['AM_PM_NIGHT'],
                          HAUL=rec['HAUL'],
                          VEHICLE='')
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
    column_names = ['RUN_ID', 'YEAR', 'MONTH', 'DATASOURCE', 'PORTROUTE', 'ARRIVEDEPART', 'TRAFFICTOTAL',
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
            if rec['DATASOURCE'] == data_source:
                ds_filtered.append(rec)

        if len(ds_filtered) == 0:
            abort(400)

        output = ds_filtered

    return jsonify(output)


@app.route('/TRAFFIC_DATA/<run_id>', methods=['DELETE'])
@app.route('/traffic_data/<run_id>', methods=['DELETE'])
def delete_traffic_data(run_id=None):
    data = TrafficData.query.filter_by(RUN_ID=run_id).all()
    for rec in data:
        db.session.delete(rec)

    db.session.commit()

    return "", 200

# UNSAMPLED OOH DATA

@app.route('/UNSAMPLED_OOH_DATA/<run_id>', methods=['POST'])
@app.route('/unsampled_ooh_data/<run_id>', methods=['POST'])
def import_unsampled_data(run_id):

    if not request.json:
        abort(400)

    data = request.json

    for rec in data:
        run = UnsampledOOHData(RUN_ID=run_id,
                               YEAR=rec['YEAR'],
                               MONTH=rec['MONTH'],
                               DATASOURCE=rec['DATASOURCE'],
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
    column_names = ['RUN_ID', 'YEAR', 'MONTH', 'DATASOURCE', 'PORTROUTE', 'REGION', 'ARRIVEDEPART', 'UNSAMP_TOTAL']

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
            if rec['DATASOURCE'] == data_source:
                ds_filtered.append(rec)

        if len(ds_filtered) == 0:
            abort(400)

        output = ds_filtered

    return jsonify(output)


@app.route('/UNSAMPLED_OOH_DATA/<run_id>', methods=['DELETE'])
@app.route('/unsampled_ooh_data/<run_id>', methods=['DELETE'])
def delete_unsampled_data(run_id=None):
    data = TrafficData.query.filter_by(RUN_ID=run_id).all()
    for rec in data:
        db.session.delete(rec)

    db.session.commit()

    return "", 200

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

@app.route('/EXPORT_DATA_DOWNLOAD', methods=['POST'])
@app.route('/export_data_download', methods=['POST'])
def create_export_data_download(run_id=None):
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
    if not request.json:
        abort(400)

    # Get json dictionary and values
    json_data = request.json
    # table_name = json_data["SOURCE_TABLE"]

    if not run_id:
        # Run Get function
        # response = function_name[table_name]()
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
                 'DATASOURCE': 'DATASOURCE', 'PORTROUTE': 'PORTROUTE', 'WEEKDAY': 'WEEKDAY',
                 'ARRIVEDEPART': 'ARRIVEDEPART', 'TOTAL': 'TOTAL', 'AM_PM_NIGHT': 'AM_PM_NIGHT'}
    json_data2 = {'RUN_ID': 'Automated-Run_ID', 'YEAR': 'YEAR-2', 'MONTH': 'MONTH-2',
                 'DATASOURCE': 'DATASOURCE-2', 'PORTROUTE': 'PORTROUTE-2', 'WEEKDAY': 'WEEKDAY-2',
                 'ARRIVEDEPART': 'ARRIVEDEPART-2', 'TOTAL': 'TOTAL-2', 'AM_PM_NIGHT': 'AM_PM_NIGHT-2'}

    output.append(json_data)
    output.append(json_data2)

    return jsonify(output)


# SURVEY SUBSAMPLE

@app.route('/SURVEY_SUBSAMPLE', methods=['GET'])
@app.route('/survey_subsample', methods=['GET'])
@app.route('/SURVEY_SUBSAMPLE/<run_id>', methods=['GET'])
@app.route('/survey_subsample/<run_id>', methods=['GET'])
def get_survey_subsample_data(run_id=None):
    column_names = ['RUN_ID', 'SERIAL', 'AGE', 'AM_PM_NIGHT', 'ANYUNDER16', 'APORTLATDEG', 'APORTLATMIN', 'APORTLATSEC',
                    'APORTLATNS', 'APORTLONDEG', 'APORTLONMIN', 'APORTLONSEC', 'APORTLONEW', 'ARRIVEDEPART', 'BABYFARE',
                    'BEFAF', 'CHANGECODE', 'CHILDFARE', 'COUNTRYVISIT', 'CPORTLATDEG', 'CPORTLATMIN', 'CPORTLATSEC',
                    'CPORTLATNS', 'CPORTLONDEG', 'CPORTLONMIN', 'CPORTLONSEC', 'CPORTLONEW', 'INTDATE', 'DAYTYPE',
                    'DIRECTLEG', 'DVEXPEND', 'DVFARE', 'DVLINECODE', 'DVPACKAGE', 'DVPACKCOST', 'DVPERSONS',
                    'DVPORTCODE', 'EXPENDCODE', 'EXPENDITURE', 'FARE', 'FAREK', 'FLOW', 'HAULKEY', 'INTENDLOS',
                    'KIDAGE', 'LOSKEY', 'MAINCONTRA', 'MIGSI', 'INTMONTH', 'NATIONALITY', 'NATIONNAME', 'NIGHTS1',
                    'NIGHTS2', 'NIGHTS3', 'NIGHTS4', 'NIGHTS5', 'NIGHTS6', 'NIGHTS7', 'NIGHTS8', 'NUMADULTS', 'NUMDAYS',
                    'NUMNIGHTS', 'NUMPEOPLE', 'PACKAGEHOL', 'PACKAGEHOLUK', 'PERSONS', 'PORTROUTE', 'PACKAGE',
                    'PROUTELATDEG', 'PROUTELATMIN', 'PROUTELATSEC', 'PROUTELATNS', 'PROUTELONDEG', 'PROUTELONMIN',
                    'PROUTELONSEC', 'PROUTELONEW', 'PURPOSE', 'QUARTER', 'RESIDENCE', 'RESPNSE', 'SEX', 'SHIFTNO',
                    'SHUTTLE', 'SINGLERETURN', 'TANDTSI', 'TICKETCOST', 'TOWNCODE1', 'TOWNCODE2', ' TOWNCODE3',
                    'TOWNCODE4', 'TOWNCODE5', 'TOWNCODE6', 'TOWNCODE7', 'TOWNCODE8', 'TRANSFER', 'UKFOREIGN', 'VEHICLE',
                    'VISITBEGAN', 'WELSHNIGHTS', 'WELSHTOWN', 'AM_PM_NIGHT_PV', 'APD_PV', 'ARRIVEDEPART_PV',
                    'CROSSINGS_FLAG_PV', 'STAYIMPCTRYLEVEL1_PV', 'STAYIMPCTRYLEVEL2_PV', 'STAYIMPCTRYLEVEL3_PV',
                    'STAYIMPCTRYLEVEL4_PV', 'DAY_PV', 'DISCNT_F1_PV', 'DISCNT_F2_PV', 'DISCNT_PACKAGE_COST_PV',
                    'DUR1_PV', 'DUR2_PV', 'DUTY_FREE_PV', 'FAGE_PV', 'FARES_IMP_ELIGIBLE_PV', 'FARES_IMP_FLAG_PV',
                    'FLOW_PV', 'FOOT_OR_VEHICLE_PV', 'HAUL_PV', 'IMBAL_CTRY_FACT_PV', 'IMBAL_CTRY_GRP_PV',
                    'IMBAL_ELIGIBLE_PV', 'IMBAL_PORT_FACT_PV', 'IMBAL_PORT_GRP_PV', 'IMBAL_PORT_SUBGRP_PV', 'LOS_PV',
                    'LOSDAYS_PV', 'MIG_FLAG_PV', 'MINS_CTRY_GRP_PV', 'MINS_CTRY_PORT_GRP_PV', 'MINS_FLAG_PV',
                    'MINS_NAT_GRP_PV', 'MINS_PORT_GRP_PV', 'MINS_QUALITY_PV', 'NR_FLAG_PV', 'NR_PORT_GRP_PV',
                    'OPERA_PV', 'OSPORT1_PV', 'OSPORT2_PV', 'OSPORT3_PV', 'OSPORT4_PV', 'PUR1_PV', 'PUR2_PV', 'PUR3_PV',
                    'PURPOSE_PV', 'QMFARE_PV', 'RAIL_CNTRY_GRP_PV', 'RAIL_EXERCISE_PV', 'RAIL_IMP_ELIGIBLE_PV',
                    'REG_IMP_ELIGIBLE_PV', 'SAMP_PORT_GRP_PV', 'SHIFT_FLAG_PV', 'SHIFT_PORT_GRP_PV',
                    'SPEND_IMP_FLAG_PV', 'SPEND_IMP_ELIGIBLE_PV', 'STAY_IMP_ELIGIBLE_PV', 'STAY_IMP_FLAG_PV',
                    'STAY_PURPOSE_GRP_PV', 'TOWNCODE_PV', 'TOWN_IMP_ELIGIBLE_PV', 'TYPE_PV', 'UK_OS_PV', 'UKPORT1_PV',
                    'UKPORT2_PV', 'UKPORT3_PV', 'UKPORT4_PV', 'UNSAMP_PORT_GRP_PV', 'UNSAMP_REGION_GRP_PV',
                    'WEEKDAY_END_PV', 'DIRECT', 'EXPENDITURE_WT', 'EXPENDITURE_WTK', 'FAREKEY', 'OVLEG', 'SPEND',
                    'SPEND1', 'SPEND2', 'SPEND3', 'SPEND4', 'SPEND5', 'SPEND6', 'SPEND7', 'SPEND8', 'SPEND9',
                    'SPENDIMPREASON', 'SPENDK', 'STAY', 'STAYK', 'STAY1K', 'STAY2K', 'STAY3K', 'STAY4K', 'STAY5K',
                    'STAY6K', 'STAY7K', 'STAY8K', 'STAY9K', 'STAYTLY', 'STAY_WT', 'STAY_WTK', 'TYPEINTERVIEW', 'UKLEG',
                    'VISIT_WT', 'VISIT_WTK', 'SHIFT_WT', 'NON_RESPONSE_WT', 'MINS_WT', 'TRAFFIC_WT',
                    'UNSAMP_TRAFFIC_WT', 'IMBAL_WT', 'FINAL_WT']

    data = SurveySubsample.query.all()

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


