import pandas
from flask import request, abort
import myapp.persistence_layer as p_layer
from myapp.app_methods import get_engine


# RUNS

def get_run(run_id=False):
    data = p_layer.get('RUN')

    output = None

    # if a run id is provided search for this specific run
    if run_id:
        # This is not and may not need to be implemented as it is dealt with user side
        pass
    else:

        output = data.to_json(orient='records')

    return output


def create_run():
    # Check if the request contains json data and an id (these must be present)
    if not request.json or 'RUN_ID' not in request.json:
        abort(400)

    # Get data dictionary from the json request
    data = request.json

    # Convert the dictionary into data frame format
    df = pandas.DataFrame(data, index=[0])

    # Writes data frame to sql
    eng = get_engine()
    df.to_sql('RUN', eng, if_exists='append', index=False)

    return "", 201


def edit_run(run_id):
    # Check if the request contains json data and an id (these must be present)
    if not request.json or not run_id:
        abort(400)

    # Get data dictionary from the json request
    data = request.json

    # Convert the dictionary into data frame format
    df = pandas.DataFrame(data, index=[0])

    # Deletes old run instance from database before inserting updated version
    p_layer.delete_from_table('RUN', 'RUN_ID', '=', str(df['RUN_ID'][0]))

    # Writes data frame to sql
    eng = get_engine()
    df.to_sql('RUN', eng, if_exists='append', index=False)

    return "", 200


# RUN_STEPS

def get_run_steps(run_id=None):

    data = p_layer.get('RUN_STEPS')

    if data.empty:
        abort(400)

    if run_id:
        data = data.loc[data['RUN_ID'] == run_id]

        if data.empty:
            abort(400)

    output = data.to_json(orient='records')

    return output


def create_run_steps(run_id):

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

    data = []

    for key, value in steps.items():
        rec = {'RUN_ID': run_id,
               'STEP_NUMBER': key,
               'STEP_NAME': value,
               'STEP_STATUS': 0}
        data.append(rec)

    # Convert the dictionary into data frame format
    df = pandas.DataFrame(data)

    # Deletes run_steps records for the active run before inserting updated step data
    p_layer.delete_from_table('RUN_STEPS', 'RUN_ID', '=', str(df['RUN_ID'][0]))

    # Writes data frame to sql
    eng = get_engine()
    df.to_sql('RUN_STEPS', eng, if_exists='append', index=False)

    return "", 201


def edit_run_steps(run_id, value, step_number=None):

    if not run_id:
        abort(400)

    if not value:
        abort(400)

    df = p_layer.get('RUN_STEPS')

    df = df.loc[df['RUN_ID'] == run_id]

    if step_number:
        df.loc[df['STEP_NUMBER'] == float(step_number), 'STEP_STATUS'] = float(value)
    else:
        df.STEP_STATUS = value

    df.index = range(0, len(df))

    # Deletes run_steps records for the active run before inserting updated step data
    p_layer.delete_from_table('RUN_STEPS', 'RUN_ID', '=', str(df['RUN_ID'][0]))

    # Writes new data to sql
    eng = get_engine()
    df.to_sql('RUN_STEPS', eng, if_exists='append', index=False)

    return "", 200


# PROCESS VARIABLE

def get_process_variables(run_id=None):

    data = p_layer.get('PROCESS_VARIABLE_PY')

    if data.empty:
        abort(400)

    if run_id:
        data = data.loc[data['RUN_ID'] == run_id]

        if data.empty:
            abort(400)

    output = data.to_json(orient='records')

    return output


def create_process_variables(run_id, template_id):

    data = get_process_variables(template_id)

    # Convert the dictionary into data frame format
    df = pandas.DataFrame(data, index=[0])

    if df.empty:
        abort(400)

    df['RUN_ID'] = run_id

    # Writes data frame to sql
    eng = get_engine()
    df.to_sql('PROCESS_VARIABLE_PY', eng, if_exists='append', index=False)

    return "", 201


def edit_process_variables():

    # the request should be json and an id must be present
    if not request.json:
        abort(400)

    updated_data = request.json


    return
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

# PROCESS VARIABLE SETS

